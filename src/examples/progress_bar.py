import asyncio
import random

import pyx
from pyx import E
from pyx.rich import run


def ProgressBar():
    completion, set_completion = pyx.use_state(0.0)
    task: pyx.Ref[asyncio.Task | None] = pyx.use_ref()

    async def update():
        actual_completion = completion
        while actual_completion < 1.0:
            await asyncio.sleep(random.random() * 0.03)
            actual_completion += random.random() * 0.02
            actual_completion = min(actual_completion, 1.0)
            set_completion(actual_completion)

    @pyx.use_effect([])
    def _():
        task.current = asyncio.create_task(update())
        return lambda: task.current.cancel()

    return E("div")[f"{completion:.2f}%"]


if __name__ == "__main__":
    run(E(ProgressBar))
