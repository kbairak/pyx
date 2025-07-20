import asyncio

import pyx
from pyx import E
from pyx.rich import run


def HelloThenWorld():
    msg, set_msg = pyx.use_state("hello")
    task: pyx.Ref[asyncio.Task | None] = pyx.use_ref()

    async def update():
        await asyncio.sleep(2)
        set_msg("hello world")

    @pyx.use_effect([])
    def _():
        task.current = asyncio.create_task(update())
        return lambda: task.current.cancel()

    return E("div")[msg]


if __name__ == "__main__":
    run(E(HelloThenWorld))
