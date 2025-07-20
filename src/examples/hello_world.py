from pyx import E, use_state
from pyx.rich import run


def HelloWorld():
    msg, _ = use_state("Hello world")
    return E("div")[msg]


if __name__ == "__main__":
    run(E(HelloWorld))
