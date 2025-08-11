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
from pyx.component import Component


@dataclass
class Renderer:
    live: Live

    @classmethod
    def draw(cls, e: E) -> Any:
        if e.tag == "div":
            return cls._draw_div(e)
        elif e.tag == "" and len(e.props) == 0:
            return cls._draw_group(e)
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

    @classmethod
    def _draw_group(cls, e: E) -> Group:
        widgets = []
        for child in e.children:
            if not child:
                continue
            elif isinstance(child, E):
                widgets.append(cls.draw(child))
            elif isinstance(child, Component):
                widgets.append(child.widget)
            else:
                raise ValueError(f"Unsupported {child=}")
        return Group(*widgets)

    @staticmethod
    def change_props(widget: Any, old_props: dict, new_props: dict):
        if isinstance(widget, Text):
            if new_props.keys() <= inspect.signature(Style).parameters.keys():
                style = Style(**new_props)
            else:
                style = new_props.get("style", "")
            widget.stylize(style)
        else:
            raise ValueError(f"Unsupported widget for props change: {type(widget)}")

    @staticmethod
    def change_text(widget: Any, old_text: str, new_text: str):
        if isinstance(widget, Text):
            widget.plain = new_text
        else:
            raise ValueError(f"Unsupported widget for text change: {type(widget)}")

    @staticmethod
    def insert_widget(parent_widget: Any, child_widget: Any, index: int):
        if isinstance(parent_widget, Group):
            parent_widget.renderables.insert(index, child_widget)
        else:
            raise ValueError(f"Unsupported parent widget for insertion: {type(parent_widget)}")

    @staticmethod
    def remove_widget(parent_widget: Any, index: int):
        if isinstance(parent_widget, Group):
            parent_widget.renderables.pop(index)
        else:
            raise ValueError(f"Unsupported parent widget for removal: {type(parent_widget)}")

    def refresh(self):
        self.live.refresh()


async def _run(e: E):
    renderer = Renderer(
        Live(console=Console(file=io.StringIO()) if os.getenv("PYX_DEBUG") else None)
    )
    component = Component(e, renderer)
    renderer.live.update(component.widget)
    renderer.live.start()
    while tasks := [t for t in asyncio.all_tasks() if t != asyncio.current_task()]:
        await asyncio.wait(tasks)
    renderer.live.stop()


def run(e: E):
    asyncio.run(_run(e))
