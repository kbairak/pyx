import enum
from dataclasses import dataclass, field
from typing import Any, Literal

from pyx.element import E

active_component: "dict[Literal['current'], None | Component]" = {"current": None}


class PatchType(enum.Enum):
    CHANGE_TEXT = enum.auto()
    INSERT_CHILD = enum.auto()


def diff(old: E, new: E) -> list:
    result = []
    if (
        old.tag == new.tag
        and old.props == new.props
        and len(old.children) == len(new.children) == 1
        and isinstance(old.children[0], str)
        and isinstance(new.children[0], str)
        and old.children[0] != new.children[0]
    ):
        result.append((PatchType.CHANGE_TEXT, new.children[0]))
    for i, (left, right) in enumerate(zip(old.children, new.children, strict=False)):
        if left is None and right is not None:
            result.append((PatchType.INSERT_CHILD, i, right))
    return result


@dataclass
class Component:
    element: E
    renderer: Any
    widget: Any = None
    state: list[Any] = field(default_factory=list)
    pointer: int | None = None
    virtual_dom: E | None = None

    def __post_init__(self):
        active_component["current"] = self
        assert callable(self.element.tag)
        self.virtual_dom = self.element.tag(*self.element.children, **self.element.props)
        active_component["current"] = None

        assert self.virtual_dom is not None
        for i, child in enumerate(list(self.virtual_dom.children)):
            if isinstance(child, E) and callable(child.tag):
                self.virtual_dom.children[i] = Component(child, self.renderer)

        self.widget = self.renderer.draw(self.virtual_dom)

    def set_state(self, index: int, value: Any) -> None:
        self.state[index] = value
        self.rerender()

    def rerender(self):
        active_component["current"] = self
        self.pointer = 0
        assert callable(self.element.tag)
        new_virtual_dom = self.element.tag(*self.element.children, **self.element.props)
        self.pointer = None
        active_component["current"] = None

        assert self.virtual_dom is not None
        patch_list = diff(self.virtual_dom, new_virtual_dom)
        for patch_type, *args in patch_list:
            if patch_type == PatchType.CHANGE_TEXT:
                (new_text,) = args
                self.renderer.update_text(self.widget, new_text)
            elif patch_type == PatchType.INSERT_CHILD:
                index, new_element = args
                if index == len(self.virtual_dom.children):
                    self.virtual_dom.children.append(None)
                elif index > len(self.virtual_dom.children):
                    raise ValueError(
                        f"Cannot insert child at index {index} in {self.virtual_dom=}"
                    )
                self.virtual_dom.children[index] = new_element
                if callable(new_element.tag):
                    self.virtual_dom.children[index] = Component(new_element, self.renderer)
                    widget = self.virtual_dom.children[index].widget
                else:
                    widget = self.renderer.draw(new_element)
                self.renderer.insert_child(self.widget, index, widget)

        self.virtual_dom = new_virtual_dom
        self.renderer.refresh()
