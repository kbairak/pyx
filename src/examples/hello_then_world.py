import asyncio

import pyx.rich
from pyx import E


def Main():
    # Equivalent to `const [msg, setMsg] = useState("hello")`
    msg, set_msg = pyx.use_state("hello")

    @pyx.use_task([])
    async def _():
        await asyncio.sleep(0.7)
        # breakpoint()
        set_msg("hello world")

    return msg


if __name__ == "__main__":
    # Equivalent to `createRoot(<HelloThenWorld />)`
    pyx.rich.run(E(Main))
    pyx.rich.run(E()[E(Main)])
    pyx.rich.run(E("div")[E(Main)])
    pyx.rich.run(E("div", style="yellow")[E(Main)])
