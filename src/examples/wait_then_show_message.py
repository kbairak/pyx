import asyncio
import random
from asyncio import Task
from collections.abc import Callable

import pyx.rich
from pyx import E


def ProgressBar(on_complete: Callable[..., None] | None = None):
    completion, set_completion = pyx.use_state(0.0)
    task: pyx.Ref[Task | None] = pyx.use_ref(None)

    @pyx.use_effect([])
    def _():
        async def _update():
            actual_completion = completion
            while actual_completion < 1.0:
                await asyncio.sleep(random.random() * 0.03)
                actual_completion += random.random() * 0.02
                actual_completion = min(actual_completion, 1.0)
                set_completion(actual_completion)
            if on_complete is not None:
                on_complete()

        task.current = asyncio.create_task(_update())

        def _callback():
            assert task.current is not None
            task.current.cancel()

        return _callback

    return E("div")[f"{completion * 100:5.2f}%"]


def Main():
    show_msg, set_show_msg = pyx.use_state(False)
    children = [E(ProgressBar, on_complete=lambda: set_show_msg(True))]
    if show_msg:
        children.append(E("div")["Hello world"])
    return E()[children]


if __name__ == "__main__":
    pyx.rich.run(E(Main))
