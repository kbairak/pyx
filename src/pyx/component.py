import enum
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Literal

from pyx.element import E

active_component: "dict[Literal['current'], None | Component]" = {"current": None}


class PatchType(enum.Enum):
    CHANGE_TEXT = enum.auto()


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
    return result


@dataclass
class Component:
    func: Callable[..., E]
    children: list[Any]
    props: dict[str, Any]

    renderer: Any

    widget: Any = None

    state: list[Any] = field(default_factory=list)
    pointer: int | None = None

    virtual_dom: E | None = None

    def __post_init__(self):
        active_component["current"] = self
        self.virtual_dom = self.func(*self.children, **self.props)
        active_component["current"] = None

        for i, child in enumerate(list(self.virtual_dom.children)):
            if isinstance(child, E) and callable(child.tag):
                self.virtual_dom.children[i] = Component(
                    child.tag, child.children, child.props, self.renderer
                )

        self.widget = self.renderer.draw(self.virtual_dom)

    def set_state(self, index: int, value: Any) -> None:
        self.state[index] = value
        self.rerender()

    def rerender(self):
        active_component["current"] = self
        self.pointer = 0
        new_virtual_dom = self.func(*self.children, **self.props)
        self.pointer = None
        active_component["current"] = None

        assert self.virtual_dom is not None
        patch_list = diff(self.virtual_dom, new_virtual_dom)
        self.widget = self.renderer.apply_patch_list(self.widget, patch_list)
        self.virtual_dom = new_virtual_dom
        self.renderer.refresh()
