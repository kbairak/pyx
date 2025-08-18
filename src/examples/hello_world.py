import pyx.rich
from pyx import E


def ReturnsString():
    msg, _ = pyx.use_state("hello world as function component that returns string")

    return msg


def ReturnsFragment():
    msg, _ = pyx.use_state("hello world as function component that returns fragment")

    return E()[msg]


def ReturnsDiv():
    msg, _ = pyx.use_state("hello world as function component that returns div")

    return E("div")[msg]


if __name__ == "__main__":
    pyx.rich.run("hello world as string")
    pyx.rich.run(E()["hello world as fragment"])
    pyx.rich.run(E("div")["hello world as div"])
    pyx.rich.run(E(ReturnsString))
    pyx.rich.run(E(ReturnsFragment))
    pyx.rich.run(E(ReturnsDiv))
