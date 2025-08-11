import asyncio
import random
from collections.abc import Callable

import pyx
from pyx import E


def ProgressBar(interval: float = 0.03, on_complete: Callable[[], None] | None = None):
    # Equivalent to `const [completion, setCompletion] = useState(0.0)`
    completion, set_completion = pyx.use_state(0.0)

    @pyx.use_task([])
    async def _():
        actual_completion = completion
        while actual_completion < 1.0:
            await asyncio.sleep(random.random() * interval)
            actual_completion = min(actual_completion + random.random() * 0.02, 1.0)
            set_completion(actual_completion)
        if on_complete is not None:
            on_complete()

    # Equivalent to `return <div>{completion * 100}%</div>`
    return E("div")[f"{completion * 100:6.2f}%"]
