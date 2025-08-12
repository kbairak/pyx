import pyx.rich
from pyx import E


def HelloWorld():
    # Equivalent to `const [msg, setMsg] = useState("hello world")`
    msg, _ = pyx.use_state("hello world")

    return E("div")[msg]  # Equivalent to `return <div>{msg}</div>`


if __name__ == "__main__":
    # Equivalent to `createRoot(<HelloWorld />)`
    pyx.rich.run(E(HelloWorld))
