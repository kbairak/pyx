import asyncio
import random

import pyx.rich
from pyx import E


def Main():
    style, set_style = pyx.use_state("")

    @pyx.use_task([])
    async def _():
        colors = ["green", "red", "yellow", "blue", "magenta", "cyan"]
        random.shuffle(colors)
        for color in colors:
            await asyncio.sleep(0.3)
            set_style(color)

    # Equivalent to `return <div style={style}>hello world</div>`
    return E("div", style=style)["hello world"]


if __name__ == "__main__":
    pyx.rich.run(E(Main))
