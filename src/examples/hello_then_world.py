import asyncio

import pyx.rich
from pyx import E


def HelloThenWorld():
    # Equivalent to `const [msg, setMsg] = useState("hello")`
    msg, set_msg = pyx.use_state("hello")

    @pyx.use_task([])
    async def _():
        await asyncio.sleep(1)
        set_msg(lambda old_str: old_str + " ")
        set_msg(lambda old_str: old_str + "world")

    return E("div")[msg]  # Equivalent to `return <div>{msg}</div>`


if __name__ == "__main__":
    # Equivalent to `createRoot(<HelloThenWorld />)`
    pyx.rich.run(E(HelloThenWorld))
