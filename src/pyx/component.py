from dataclasses import dataclass, field
from typing import Any

from pyx.element import E
from pyx.utils import defer, singleton


@singleton
@dataclass
class active:
    component: "Component | None" = None
    pointer: int | None = None
    renderer: Any = None


@dataclass
class Component:
    element: E
    widget: Any = None
    state: list[Any] = field(default_factory=list)
    virtual_dom: E | None = None
    _dirty: bool = False

    def __post_init__(self):
        active.component = self
        assert callable(self.element.tag)
        self.virtual_dom = self.element.tag(*self.element.children, **self.element.props)
        active.component = None

        assert self.virtual_dom is not None
        for i, child in enumerate(list(self.virtual_dom.children)):
            if isinstance(child, E) and callable(child.tag):
                self.virtual_dom.children[i] = Component(child)

        self.widget = active.renderer.draw(self.virtual_dom)

    def set_state(self, index: int, value: Any) -> None:
        self.state[index] = (value,)
        if not self._dirty:
            self._dirty = True

            @defer
            async def _():
                if not self._dirty:
                    return

                active.component = self
                active.pointer = 0
                assert callable(self.element.tag)
                new_virtual_dom = self.element.tag(*self.element.children, **self.element.props)
                active.pointer = None
                active.component = None

                assert self.virtual_dom is not None
                if self.virtual_dom.tag != new_virtual_dom.tag:
                    # TODO: Must inform parent to replace me
                    raise NotImplementedError("Changing tag is not supported yet")

                if (old_props := self.virtual_dom.props) != (new_props := new_virtual_dom.props):
                    # Must tell renderer to change my props
                    active.renderer.change_props(self.widget, old_props, new_props)

                if (
                    len(self.virtual_dom.children) == len(new_virtual_dom.children) == 1
                    and isinstance((old_text := self.virtual_dom.children[0]), str)
                    and isinstance((new_text := new_virtual_dom.children[0]), str)
                ):
                    active.renderer.change_text(self.widget, old_text, new_text)

                else:
                    for i, (left, right) in enumerate(
                        zip(self.virtual_dom.children, new_virtual_dom.children, strict=False)
                    ):
                        if not left and right:
                            if isinstance(right, E):
                                if callable(right.tag):
                                    new_virtual_dom.children[i] = Component(right)
                                    active.renderer.insert_widget(
                                        self.widget, new_virtual_dom.children[i].widget, i
                                    )
                                else:
                                    widget = active.renderer.draw(right)
                                    active.renderer.insert_widget(self.widget, widget, i)
                            elif isinstance(right, str):
                                raise NotImplementedError(
                                    "Adding text elements is not supported yet"
                                )
                            else:
                                raise ValueError(f"Unsupported right child: {right}")
                        elif left and not right:
                            if isinstance(left, Component):
                                left.unmount()
                            active.renderer.remove_widget(
                                self.widget,
                                i - sum(1 for child in new_virtual_dom.children[:i] if not child),
                            )

                self.virtual_dom = new_virtual_dom
                active.renderer.refresh()

                self._dirty = False

    def unmount(self):
        if self.virtual_dom is not None:
            for child in self.virtual_dom.children:
                if isinstance(child, Component):
                    child.unmount()
        for state in self.state:
            try:
                _, callback = state
            except ValueError:
                # Not an effect
                continue
            if callback is not None:
                callback()
