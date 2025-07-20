from rich.text import Text

from pyx.element import E
from pyx.rich import draw


def test_simple_span():
    assert draw(E("div")["Hello, World!"]) == Text("Hello, World!")
