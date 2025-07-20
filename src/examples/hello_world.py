import pyx.rich
from pyx import E


def HelloWorld():
    # Equivalent to `const [msg, setMsg] = useState("Hello world")`
    msg, _ = pyx.use_state("Hello world")

    return E("div")[msg]  # Equivalent to <div>{msg}</div>


if __name__ == "__main__":
    pyx.rich.run(E(HelloWorld))  # Equivalent to createRoot(<HelloWorld />)
