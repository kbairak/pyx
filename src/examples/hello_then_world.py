import asyncio

import pyx.rich
from pyx import E


def HelloThenWorld():
    # Equivalent to `const [msg, setMsg] = useState("hello")`
    msg, set_msg = pyx.use_state("hello")

    # Equivalent to `const task = useRef()`
    task: pyx.Ref[asyncio.Task | None] = pyx.use_ref()

    # Equivalent to `useEffect(() => { ... }, [])`
    @pyx.use_effect([])
    def _():
        async def _update():
            await asyncio.sleep(2)
            set_msg("hello world")

        task.current = asyncio.create_task(_update())

        def _callback():
            assert task.current is not None
            task.current.cancel()

        return _callback

    return E("div")[msg]  # Equivalent to `return <div>{msg}</div>`


if __name__ == "__main__":
    # Equivalent to `createRoot(<HelloThenWorld />)`
    pyx.rich.run(E(HelloThenWorld))
