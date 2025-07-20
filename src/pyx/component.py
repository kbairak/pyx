from collections.abc import Callable
from copy import copy
from dataclasses import dataclass, field
from typing import Any, Literal

from pyx.element import E

active_component: "dict[Literal['current'], None | Component]" = {"current": None}


@dataclass
class Component:
    func: Callable[..., E]
    parent: Any = None
    state: list[Any] = field(default_factory=list)
    pointer: int | None = None

    virtual_dom_as_returned: E | None = None
    virtual_dom_with_components: E | None = None
    virtual_dom_fully_expanded: E | None = None

    def first_render(self) -> E:
        active_component["current"] = self
        self.virtual_dom_as_returned = self.func()
        active_component["current"] = None

        self.virtual_dom_with_components = copy(self.virtual_dom_as_returned)
        self.virtual_dom_fully_expanded = copy(self.virtual_dom_as_returned)
        for i, e in enumerate(self.virtual_dom_as_returned.children):
            if not isinstance(e, E) or not callable(e.tag):
                continue
            component = Component(e.tag, self)
            inner_dom = component.first_render()
            self.virtual_dom_with_components.children[i] = component
            self.virtual_dom_fully_expanded.children[i] = inner_dom

        return self.virtual_dom_fully_expanded

    def set_state(self, index: int, value: Any) -> None:
        self.state[index] = value
        if isinstance(self.parent, Component):
            self.parent.rerender()
        else:
            self.rerender()

    def rerender(self) -> E:
        active_component["current"] = self
        self.pointer = 0
        self.virtual_dom_as_returned = self.func()
        self.pointer = None
        active_component["current"] = None

        self.virtual_dom_fully_expanded = copy(self.virtual_dom_as_returned)
        for i, e in enumerate(self.virtual_dom_as_returned.children):
            if not isinstance(e, E) or not callable(e.tag):
                continue
            assert self.virtual_dom_with_components is not None
            component = self.virtual_dom_with_components.children[i]
            inner_dom = component.rerender()
            assert self.virtual_dom_fully_expanded is not None
            self.virtual_dom_fully_expanded.children[i] = inner_dom

        if not isinstance(self.parent, Component):
            self.parent.update(self.virtual_dom_fully_expanded)

        return self.virtual_dom_fully_expanded
