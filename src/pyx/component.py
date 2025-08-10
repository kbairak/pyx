from dataclasses import dataclass, field
from typing import Any, Literal

from pyx.element import E

active_component: "dict[Literal['current'], Component | None]" = {"current": None}


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
        if self.virtual_dom.tag != new_virtual_dom.tag:
            # TODO: Must inform parent to replace me
            raise NotImplementedError("Changing tag is not supported yet")

        if (old_props := self.virtual_dom.props) != (new_props := new_virtual_dom.props):
            # Must tell renderer to change my props
            self.renderer.change_props(self.widget, old_props, new_props)

        if (
            len(self.virtual_dom.children) == len(new_virtual_dom.children) == 1
            and isinstance((old_text := self.virtual_dom.children[0]), str)
            and isinstance((new_text := new_virtual_dom.children[0]), str)
        ):
            self.renderer.change_text(self.widget, old_text, new_text)

        else:
            for i, (left, right) in enumerate(
                zip(self.virtual_dom.children, new_virtual_dom.children, strict=False)
            ):
                if not left and right is not None:
                    if isinstance(right, E):
                        if callable(right.tag):
                            new_virtual_dom.children[i] = Component(right, self.renderer)
                            self.renderer.insert_widget(
                                self.widget, new_virtual_dom.children[i].widget, i
                            )
                        else:
                            widget = self.renderer.draw(right)
                            self.renderer.insert_widget(self.widget, widget, i)
                    elif isinstance(right, str):
                        raise NotImplementedError("Adding text elements is not supported yet")
                    else:
                        raise ValueError(f"Unsupported right child: {right}")
                elif left is not None and not right:
                    if isinstance(left, Component):
                        raise NotImplementedError("Removing components is not supported yet")
                    else:
                        self.renderer.remove_widget(
                            self.widget,
                            i - sum(1 for child in new_virtual_dom.children[:i] if not child),
                        )

        self.virtual_dom = new_virtual_dom
        self.renderer.refresh()
