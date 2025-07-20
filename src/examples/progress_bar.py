import argparse
import asyncio
import random

import pyx
from pyx import E
from pyx.rich import run


def ProgressBar(interval=0.03):
    completion, set_completion = pyx.use_state(0.0)
    task: pyx.Ref[asyncio.Task | None] = pyx.use_ref()

    async def update():
        actual_completion = completion
        while actual_completion < 1.0:
            await asyncio.sleep(random.random() * interval)
            actual_completion += random.random() * 0.02
            actual_completion = min(actual_completion, 1.0)
            set_completion(actual_completion)

    @pyx.use_effect([])
    def _():
        task.current = asyncio.create_task(update())
        return lambda: task.current.cancel()

    # Equivalent to `return <div>{completion * 100}%</div>`
    return E("div")[f"{completion * 100:.2f}%"]


parser = argparse.ArgumentParser(description="Progress bar example")
parser.add_argument("--interval", type=float, default=0.03, help="Interval in seconds (float)")

if __name__ == "__main__":
    args = parser.parse_args()

    # Equivalent to `createRoot(<ProgressBar interval={interval} />)`
    run(E(ProgressBar, interval=args.interval))
