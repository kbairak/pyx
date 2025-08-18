import os
import random

import pytest

import pyx.rich
from pyx import E
from pyx.node import active


@pytest.fixture
def getvalue():
    os.environ["PYX_DEBUG"] = "1"
    return lambda: active.renderer.live.console.file.getvalue()


def test_string(getvalue):
    pyx.rich.run("hello world as string")
    assert getvalue() == "hello world as string"


def test_fragment(getvalue):
    pyx.rich.run(E()["hello world as fragment"])
    assert getvalue() == "hello world as fragment"


def test_div(getvalue):
    pyx.rich.run(E("div")["hello world as div"])
    assert getvalue() == "hello world as div"


def test_group(getvalue):
    pyx.rich.run(E()["hello", "world"])
    assert getvalue() == "hello\nworld"


def test_function(getvalue):
    def Main():
        return "hello world"

    pyx.rich.run(E(Main))
    assert getvalue() == "hello world"


def test_nested_function(getvalue):
    def Indented(children):
        return f"  {children}"

    pyx.rich.run(E()["hello", E(Indented)["world"]])
    assert getvalue() == "hello\n  world"


def test_color(getvalue):
    pyx.rich.run(E("div", style="red")["hello world as red"])
    assert getvalue() == "hello world as red"


def test_random_color(getvalue):
    def FunnyColor():
        return random.choice(["red", "yellow"])

    pyx.rich.run(E("div", style=E(FunnyColor))["hello world as funny text"])
    assert getvalue() == "hello world as funny text"
