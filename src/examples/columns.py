import asyncio

import pyx.rich
from pyx import E


def Main():
    show, set_show = pyx.use_state([True] * 10)
    expand, set_expand = pyx.use_state(False)

    @pyx.use_task([])
    async def _():
        await asyncio.sleep(0.4)
        set_show([False] * 1 + [True] * 9)
        set_expand(lambda prev: not prev)

        await asyncio.sleep(0.4)
        set_show([False] * 3 + [True] * 7)
        set_expand(lambda prev: not prev)

        await asyncio.sleep(0.4)
        set_show([False] * 4 + [True] * 6)
        set_expand(lambda prev: not prev)

        await asyncio.sleep(0.4)
        set_show([False] * 5 + [True] * 5)
        set_expand(lambda prev: not prev)

        await asyncio.sleep(0.4)
        set_show([False] * 6 + [True] * 4)
        set_expand(lambda prev: not prev)

        await asyncio.sleep(0.4)
        set_show([False] * 7 + [True] * 3)
        set_expand(lambda prev: not prev)

        await asyncio.sleep(0.4)
        set_show([False] * 8 + [True] * 2)
        set_expand(lambda prev: not prev)

    return E("columns", expand=expand, title="the title")[
        show[0] and "zero",
        show[1] and "one",
        show[2] and "two",
        show[3] and "three",
        show[4] and "four",
        show[5] and "five",
        show[6] and "six",
        show[7] and "seven",
        show[8] and "eight",
        show[9] and "nine",
    ]


if __name__ == "__main__":
    pyx.rich.run(E(Main))
