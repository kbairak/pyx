import asyncio
import io
import reprlib
from dataclasses import dataclass
from typing import Any

from rich.console import Console, Group
from rich.live import Live
from rich.text import Text

from pyx import E
from pyx.component import Component


def _draw(e: E) -> Any:
    if (
        e.tag == "div"
        and len(e.children) == 1
        and isinstance(e.children[0], str)
        and len(e.props) == 0
    ):
        return Text(e.children[0])
    elif e.tag == "" and len(e.props) == 0:
        widgets = []
        for child in e.children:
            if child is None:
                continue
            elif isinstance(child, E):
                widgets.append(_draw(child))
            elif isinstance(child, Component):
                widgets.append(child.widget)
            else:
                raise ValueError(f"Unsupported {child=}")
        return Group(*widgets)
    raise ValueError(f"Unsupported element: {reprlib.Repr(maxstring=70).repr(str(e))}")


def _update_text(widget: Any, new_text: str) -> None:
    if isinstance(widget, Text):
        widget.plain = new_text
    else:
        raise ValueError(f"Cannot apply {new_text=} to {widget=}")


def _insert_child(parent: Any, index: int, child: Any) -> None:
    if isinstance(parent, Group):
        if index < len(parent.renderables):
            parent.renderables[index] = child
        elif index == len(parent.renderables):
            parent.renderables.append(child)
        else:
            raise ValueError(f"Cannot insert child at index {index} in {parent=}")


@dataclass
class Renderer:
    live: Live

    @staticmethod
    def draw(e: E) -> Any:
        return _draw(e)

    @staticmethod
    def update_text(widget: Any, new_text: str) -> None:
        _update_text(widget, new_text)

    @staticmethod
    def insert_child(parent: Any, index: int, child: Any) -> None:
        _insert_child(parent, index, child)

    def refresh(self):
        self.live.refresh()


async def _run(e: E, file: io.IOBase | None = None):
    assert callable(e.tag)
    renderer = Renderer(Live(console=Console(file=io.StringIO()) if file is not None else None))
    component = Component(e, renderer)
    renderer.live.update(component.widget)
    renderer.live.start()
    while len(tasks := [t for t in asyncio.all_tasks() if t != asyncio.current_task()]) > 0:
        await asyncio.wait(tasks)
    renderer.live.stop()


def run(e: E, file: io.IOBase | None = None):
    asyncio.run(_run(e, file))
