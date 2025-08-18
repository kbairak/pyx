from asyncio import create_task
from collections.abc import MutableMapping, MutableSequence
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from pyx.element import E
from pyx.utils import singleton


@singleton
@dataclass
class active:
    node: "Node | None" = None
    pointer: int | None = None
    renderer: Any = None

    @contextmanager
    def active_node(self, node):
        self.node = node
        yield
        self.node = None

    @contextmanager
    def active_node_and_pointer(self, node):
        self.node = node
        self.pointer = 0
        yield
        self.pointer = None
        self.node = None


class Node:
    def __init__(self, element, parent):
        # value is:
        #   - a node if tag is callable
        #   - the element's props if tag is an element (expanded)
        #   - the literal value if tag is LITERAL
        if isinstance(element, E):
            self.tag = element.tag
            self.props = deepcopy(element.props)

            if callable(element.tag):
                self.state = []
                with active.active_node(self):
                    result = element.tag(**self.props)
                self.value = Node(result, self)
            else:
                self.value = self._convert_elements_to_nodes(element.props)
                self.state = None
        else:
            self.tag = "LITERAL"
            self.props = {}
            self.state = None
            self.value = element

        self.parent = parent
        self._widget: Any = None
        self._dirty = False

    def _convert_elements_to_nodes(self, obj):
        if isinstance(obj, E):
            obj = Node(obj, self)
        elif isinstance(obj, MutableSequence) and not isinstance(obj, str):
            obj = [self._convert_elements_to_nodes(item) for item in obj]
            # for i, item in list(enumerate(obj)):
            #     obj[i] = self._convert_elements_to_nodes(item)
        elif isinstance(obj, MutableMapping):
            obj = {key: self._convert_elements_to_nodes(value) for key, value in obj.items()}
            # for key, value in list(obj.items()):
            #     obj[key] = self._convert_elements_to_nodes(value)
        elif not isinstance(obj, Node):
            obj = Node(obj, self)
        return obj

    @property
    def widget(self):
        if self._widget is None:
            if self.tag == "LITERAL":
                self._widget = self.value
            elif callable(self.tag):
                assert isinstance(self.value, Node)
                self._widget = self.value.widget
            else:
                self._widget = active.renderer.draw(self)
        return self._widget

    def set_state(self, index: int, value: Any):
        assert isinstance(self.state, list)
        old_state = list(self.state)
        self.state[index] = (value,)
        if self.state != old_state and not self._dirty:
            self._dirty = True
            create_task(self.rerender())

    async def rerender(self):
        assert isinstance(self.value, Node) and callable(self.tag)
        with active.active_node_and_pointer(self):
            result = self.tag(**self.props)

        self.diff(self.value, result)

        active.renderer.rerender()
        self._dirty = False

    def diff(self, left, right):
        if (
            (left.tag == "LITERAL" and left.value != right)
            or (isinstance(right, E) and left.tag != right.tag)
            or (left.tag != "LITERAL" and not isinstance(right, E))
        ):
            if callable(left.tag):
                left.unmount()
            self._widget = None
            self.value = Node(right, left.parent)
            active.renderer.replace_widget(self.value)

    def unmount(self):
        pass

    @classmethod
    def from_values(cls, parent, tag, value, props=None, state=None):
        result = cls(None, parent)
        result.tag = tag
        if props is None:
            result.props = {}
        else:
            result.props = props
        result.state = state
        result.value = value
        return result

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (
            self.tag == other.tag
            and self.props == other.props
            and self.state == other.state
            and self.value == other.value
            and self.parent is other.parent
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(tag={self.tag!r}, value={self.value!r}, ...)"
