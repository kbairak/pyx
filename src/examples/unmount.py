import asyncio

import pyx.rich
from examples.progress_bar import ProgressBar
from pyx import E


def Main():
    show_progress_bar, set_show_progress_bar = pyx.use_state(True)

    @pyx.use_task([])
    async def _():
        await asyncio.sleep(0.5)
        set_show_progress_bar(False)

    return E()[E(ProgressBar) if show_progress_bar else None]


if __name__ == "__main__":
    pyx.rich.run(E(Main))
