import asyncio
import random

import rich.box

import pyx.rich
from pyx import E


def Main():
    box, set_box = pyx.use_state(rich.box.ROUNDED)

    @pyx.use_task([])
    async def _():
        boxes = [
            rich.box.ASCII,
            rich.box.ASCII2,
            rich.box.ASCII_DOUBLE_HEAD,
            rich.box.DOUBLE,
            rich.box.DOUBLE_EDGE,
            rich.box.HEAVY,
            rich.box.HEAVY_EDGE,
            rich.box.HEAVY_HEAD,
            rich.box.HORIZONTALS,
            rich.box.MARKDOWN,
            rich.box.MINIMAL,
            rich.box.MINIMAL_DOUBLE_HEAD,
            rich.box.MINIMAL_HEAVY_HEAD,
            rich.box.ROUNDED,
            rich.box.SIMPLE,
            rich.box.SIMPLE_HEAD,
            rich.box.SIMPLE_HEAVY,
            rich.box.SQUARE,
            rich.box.SQUARE_DOUBLE_HEAD,
        ]
        random.shuffle(boxes)
        for box in boxes:
            await asyncio.sleep(0.2)
            set_box(box)

    return E("panel", expand=False, box=box, title="hello", subtitle="world")["Hello world"]


if __name__ == "__main__":
    pyx.rich.run(E(Main))  # Equivalent to createRoot(<Main />)
