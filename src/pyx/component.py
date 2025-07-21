import enum
from dataclasses import dataclass, field
from typing import Any, Literal

from pyx.element import E

active_component: "dict[Literal['current'], None | Component]" = {"current": None}


class PatchType(enum.Enum):
    CHANGE_TEXT = enum.auto()
    REPLACE_CHILD = enum.auto()
    SET_PROP = enum.auto()
    REMOVE_PROP = enum.auto()


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
    for key in old.props.keys() | new.props.keys():
        if key in new.props and (key not in old.props or old.props[key] != new.props[key]):
            result.append((PatchType.SET_PROP, key, new.props[key]))
        elif key not in new.props:
            result.append((PatchType.REMOVE_PROP, key, None))
    for i, (left, right) in enumerate(zip(old.children, new.children, strict=False)):
        if left is None and right is not None:
            result.append((PatchType.REPLACE_CHILD, i, right))
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
        active_component["current"] = self
        self.pointer = 0
        assert callable(self.element.tag)
        new_virtual_dom = self.element.tag(*self.element.children, **self.element.props)
        self.pointer = None
        active_component["current"] = None

        assert self.virtual_dom is not None
        for patch in diff(self.virtual_dom, new_virtual_dom):
            patch_type, *args = patch
            if patch_type in (PatchType.CHANGE_TEXT, PatchType.SET_PROP, PatchType.REMOVE_PROP):
                self.renderer.apply_patch(self.widget, patch)
            elif patch_type == PatchType.REPLACE_CHILD:
                index, new_element = args
                if index > len(self.virtual_dom.children):
                    raise ValueError(
                        f"Cannot replace child at index {index} in {self.virtual_dom=}"
                    )
                self.virtual_dom.children[index] = new_element
                if callable(new_element.tag):
                    self.virtual_dom.children[index] = Component(new_element, self.renderer)
                    widget = self.virtual_dom.children[index].widget
                else:
                    widget = self.renderer.draw(new_element)
                self.renderer.replace_child(self.widget, index, widget)

        self.virtual_dom = new_virtual_dom
        self.renderer.refresh()
