import asyncio
import reprlib
from dataclasses import dataclass
from typing import Any

from rich import print
from rich.console import Group
from rich.live import Live
from rich.text import Text

from pyx import E
from pyx.component import Component


def draw(e: E) -> Any:
    if e.tag == "" and len(e.props) == 0:
        return Group(*[draw(child) for child in e.children])
    elif e.tag == "div" and len(e.children) == 1 and isinstance(e.children[0], str):
        return Text(e.children[0])
    raise ValueError(f"Unsupported element: {reprlib.repr(str(e))}")


@dataclass
class Root:
    live: Live

    def update(self, e: E):
        self.live.update(draw(e))


async def _run(e: E):
    if not callable(e.tag):
        print(draw(e))
        return

    live = Live()
    root = Root(live)
    component = Component(e.tag, e.children, e.props, root, root)
    live.update(draw(component.virtual_dom_fully_expanded))
    live.start()
    while True:
        all_tasks = asyncio.all_tasks()
        tasks = [t for t in all_tasks if t != asyncio.current_task()]
        if len(tasks) == 0:
            break
        await asyncio.wait(tasks)
    live.stop()


def run(e: E):
    asyncio.run(_run(e))
