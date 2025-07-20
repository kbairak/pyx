import asyncio
import reprlib
from dataclasses import dataclass
from typing import Any

from rich.console import Group
from rich.live import Live
from rich.text import Text

from pyx import E
from pyx.component import Component, PatchType


def _draw(e: E) -> Any:
    if e.tag == "div" and len(e.children) == 1 and isinstance(e.children[0], str):
        return Text(e.children[0])
    elif e.tag == "" and len(e.props) == 0:
        widgets = []
        for child in e.children:
            if isinstance(child, E):
                widgets.append(_draw(child))
            elif isinstance(child, Component):
                widgets.extend(child.widget)
            else:
                raise ValueError(f"Unsupported {child=}")
        return Group(*widgets)
    raise ValueError(f"Unsupported element: {reprlib.Repr(maxstring=70).repr(str(e))}")


def _apply_patch_list(widget: Any, patch_list: list):
    for patch_type, *args in patch_list:
        if isinstance(widget, Text) and patch_type == PatchType.CHANGE_TEXT:
            widget.plain = args[0]
        else:
            raise ValueError(f"Cannot apply patch: {(patch_type, args)=}")
    return widget


@dataclass
class Renderer:
    live: Live

    @staticmethod
    def draw(e: E) -> Any:
        return _draw(e)

    @staticmethod
    def apply_patch_list(widget: Any, patch_list: list):
        return _apply_patch_list(widget, patch_list)

    def refresh(self):
        self.live.refresh()


async def _run(e: E):
    renderer = Renderer(Live())
    assert callable(e.tag)
    component = Component(e.tag, e.children, e.props, renderer)
    renderer.live.update(component.widget)
    renderer.live.start()
    while True:
        all_tasks = asyncio.all_tasks()
        tasks = [t for t in all_tasks if t != asyncio.current_task()]
        if len(tasks) == 0:
            break
        await asyncio.wait(tasks)
    renderer.live.stop()


def run(e: E):
    asyncio.run(_run(e))
