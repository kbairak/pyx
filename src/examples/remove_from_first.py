import asyncio

import pyx.rich
from pyx import E


def Inner(content):
    return E("div")[f"--{content}--"]


def Main():
    # Component managing a state variable with 4 booleans
    visibility, set_visibility = pyx.use_state([True, True, True, True])

    @pyx.use_task([])
    async def _():
        await asyncio.sleep(1)
        set_visibility([False, True, True, True])
        await asyncio.sleep(1)
        set_visibility([False, False, True, True])
        await asyncio.sleep(1)
        set_visibility([False, False, False, True])

    return E()[
        E(Inner)["one"] if visibility[0] else None,
        E(Inner)["two"] if visibility[1] else None,
        E(Inner)["three"] if visibility[2] else None,
        E(Inner)["four"] if visibility[3] else None,
    ]


if __name__ == "__main__":
    pyx.rich.run(E(Main))
