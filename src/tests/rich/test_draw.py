from rich.console import Group
from rich.text import Text

from pyx import E
from pyx.rich import Renderer


def test_simple_span():
    assert Renderer.draw(E("div")["Hello, World!"]) == Text("Hello, World!")


def test_fragment():
    left = Renderer.draw(E()[E("div")["hello"], E("div")["world"]])
    right = Group(Text("hello"), Text("world"))
    assert left.__dict__ == right.__dict__
