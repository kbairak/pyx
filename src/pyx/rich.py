import asyncio
import io
import os
from collections.abc import Mapping, MutableMapping, Sequence
from dataclasses import dataclass

from rich.console import Console, Group
from rich.live import Live
from rich.text import Text

from pyx import E
from pyx.node import Node, active
from pyx.utils import is_list


@dataclass
class Renderer:
    live: Live

    @classmethod
    def draw(cls, node: Node):
        props = cls._convert_nodes_to_widgets(node.value)
        assert isinstance(props, MutableMapping)
        children = props.pop("children", "")
        if node.tag == "div":
            assert isinstance(children, str)
            return Text(children, **props)
        elif node.tag == "":
            if is_list(children):
                children = [child for child in children if child not in (None, False)]
            if "fit" in props and (
                isinstance(children, str) or not isinstance(children, Sequence)
            ):
                children = [children]

            if isinstance(children, Sequence) and not isinstance(children, str):
                return Group(*children, **props)
            else:
                return children
        else:
            raise ValueError(f"Unsupported node tag: {node.tag}")

    @classmethod
    def _convert_nodes_to_widgets(cls, obj):
        if isinstance(obj, Node):
            obj = obj.widget
        elif isinstance(obj, Sequence) and not isinstance(obj, str):
            obj = [cls._convert_nodes_to_widgets(item) for item in obj]
        elif isinstance(obj, Mapping):
            obj = {k: cls._convert_nodes_to_widgets(v) for k, v in obj.items()}
        return obj

    def replace_widget(self, node: Node) -> None:
        node._widget = None

        if node.parent is self:
            self.live.update(node.widget)
        elif isinstance(node.parent.widget, Text):
            node.parent.widget.plain = node.widget
        elif isinstance(node.parent.widget, Group):
            prev_children = node.parent.value["children"]
            widget_index = 0
            for child in prev_children:
                if child is node:
                    break
                if child.widget not in (None, False):
                    widget_index += 1
            if node.widget not in (None, False):
                node.parent.widget._renderables[widget_index] = node.widget
            else:
                del node.parent.widget._renderables[widget_index]
        else:
            self.replace_widget(node.parent)

    def rerender(self):
        self.live.refresh()


def run(e):
    asyncio.run(_run(e))


async def _run(e: E):
    active.renderer = Renderer(
        Live(console=Console(file=io.StringIO()) if os.getenv("PYX_DEBUG") else None)
    )
    root_node = Node(e, active.renderer)
    active.renderer.live.update(root_node.widget)
    active.renderer.live.start()
    while tasks := [t for t in asyncio.all_tasks() if t != asyncio.current_task()]:
        await asyncio.wait(tasks)
    active.renderer.live.stop()
