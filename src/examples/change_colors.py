import asyncio
import random

import pyx.rich
from pyx import E

COLORS = ["green", "red", "yellow", "blue", "magenta", "cyan"]


def Main():
    style, set_style = pyx.use_state(random.choice(COLORS))

    @pyx.use_task([])
    async def _():
        for _ in range(5):
            await asyncio.sleep(0.3)
            set_style(random.choice(COLORS))

    # Equivalent to `return <div style={style}>hello world</div>`
    return E("div", style=style)["hello world"]


if __name__ == "__main__":
    pyx.rich.run(E(Main))
