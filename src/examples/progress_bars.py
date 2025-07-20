import asyncio
import random

import pyx.rich
from pyx import E


def ProgressBar(interval=0.03):
    # Equivalent to `const [completion, setCompletion] = useState(0.0)`
    completion, set_completion = pyx.use_state(0.0)

    # Equivalent to `const task = useRef()`
    task: pyx.Ref[asyncio.Task | None] = pyx.use_ref()

    async def update():
        actual_completion = completion
        while actual_completion < 1.0:
            await asyncio.sleep(random.random() * interval)
            actual_completion += random.random() * 0.02
            actual_completion = min(actual_completion, 1.0)
            set_completion(actual_completion)

    # Equivalent to `useEffect(() => { ... }, [])`
    @pyx.use_effect([])
    def _():
        task.current = asyncio.create_task(update())
        return lambda: task.current.cancel()

    # Equivalent to `return <div>{completion * 100}%</div>`
    return E("div")[f"{completion * 100:.2f}%"]


def Main():
    # Equivalent to `return (
    #   <>
    #     <ProgressBar interval={0.03} />
    #     <ProgressBar interval={0.04} />
    #     <ProgressBar interval={0.05} />
    #     <ProgressBar interval={0.06} />
    #   </>
    # )`
    return E()[
        E(ProgressBar, interval=0.03),
        E(ProgressBar, interval=0.04),
        E(ProgressBar, interval=0.05),
        E(ProgressBar, interval=0.06),
    ]


if __name__ == "__main__":
    pyx.rich.run(E(Main))  # Equivalent to createRoot(<Main />)
