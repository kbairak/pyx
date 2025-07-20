import asyncio

import pyx.rich
from pyx import E


def HelloThenWorld():
    # Equivalent to `const [msg, setMsg] = useState("hello")`
    msg, set_msg = pyx.use_state("hello")

    # Equivalent to `const task = useRef()`
    task: pyx.Ref[asyncio.Task | None] = pyx.use_ref()

    async def update():
        await asyncio.sleep(2)
        set_msg("hello world")

    # Equivalent to `useEffect(() => { ... }, [])`
    @pyx.use_effect([])
    def _():
        task.current = asyncio.create_task(update())
        return lambda: task.current.cancel()

    return E("div")[msg]  # Equivalent to `return <div>{msg}</div>`


if __name__ == "__main__":
    # Equivalent to `createRoot(<HelloThenWorld />)`
    pyx.rich.run(E(HelloThenWorld))
