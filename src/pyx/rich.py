import asyncio
import inspect
import io
import os
import reprlib
from dataclasses import dataclass
from typing import Any

from rich.console import Console, Group
from rich.live import Live
from rich.style import Style
from rich.text import Text

from pyx import E
from pyx.component import Component, PatchType


@dataclass
class Renderer:
    live: Live

    @classmethod
    def draw(cls, e: E) -> Any:
        if e.tag == "div":
            return cls._draw_div(e)
        elif e.tag == "" and len(e.props) == 0:
            widgets = []
            for child in e.children:
                if child is None:
                    continue
                elif isinstance(child, E):
                    widgets.append(cls.draw(child))
                elif isinstance(child, Component):
                    widgets.append(child.widget)
                else:
                    raise ValueError(f"Unsupported {child=}")
            return Group(*widgets)
        raise ValueError(f"Unsupported element: {reprlib.Repr(maxstring=70).repr(str(e))}")

    @staticmethod
    def _draw_div(e):
        if len(e.children) != 1 or not isinstance(e.children[0], str):
            raise ValueError(f"Unsupported div: {reprlib.Repr(maxstring=70).repr(str(e))}")

        if e.props.keys() <= inspect.signature(Style).parameters.keys():
            style = Style(**e.props)
        else:
            style = e.props.get("style", "")
        return Text(e.children[0], style)

    @staticmethod
    def apply_patch(widget: Any, patch) -> None:
        patch_type, *args = patch
        if patch_type == PatchType.CHANGE_TEXT and isinstance(widget, Text):
            (new_text,) = args
            widget.plain = new_text
        elif (
            patch_type == PatchType.SET_PROP
            and isinstance(widget, Text)
            and len(args) == 2
            and args[0] == "style"
        ):
            widget.stylize(args[1])
        else:
            raise ValueError(f"Cannot apply {patch=} to {widget=}")

    @staticmethod
    def replace_child(parent: Any, index: int, child: Any):
        if isinstance(parent, Group):
            # TODO: Handle empty children
            parent.renderables.extend([child] * (index - len(parent.renderables) + 1))
            parent.renderables[index] = child
        else:
            raise ValueError(f"Cannot replace {child=} in {parent=} in {index=}")

    def refresh(self):
        self.live.refresh()


async def _run(e: E):
    renderer = Renderer(
        Live(console=Console(file=io.StringIO()) if os.getenv("PYX_DEBUG") else None)
    )
    component = Component(e, renderer)
    renderer.live.update(component.widget)
    renderer.live.start()
    while len(tasks := [t for t in asyncio.all_tasks() if t != asyncio.current_task()]) > 0:
        await asyncio.wait(tasks)
    renderer.live.stop()


def run(e: E):
    asyncio.run(_run(e))
