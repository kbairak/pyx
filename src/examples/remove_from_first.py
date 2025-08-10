import asyncio

import pyx.rich
from pyx import E


def Main():
    # Component managing a state variable with 4 booleans
    visibility, set_visibility = pyx.use_state([True, True, True, True])

    @pyx.use_task([])
    async def _():
        await asyncio.sleep(0.5)
        set_visibility([False, True, True, True])
        await asyncio.sleep(0.5)
        set_visibility([False, False, True, True])
        await asyncio.sleep(0.5)
        set_visibility([False, False, False, True])

    return E()[
        E("div")["one"] if visibility[0] else None,
        E("div")["two"] if visibility[1] else None,
        E("div")["three"] if visibility[2] else None,
        E("div")["four"] if visibility[3] else None,
    ]


if __name__ == "__main__":
    pyx.rich.run(E(Main))
