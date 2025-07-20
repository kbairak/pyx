from pyx import E


def test_fragment():
    assert str(E()) == "< />"


def test_single():
    assert str(E("a")) == "<a />"
    assert str(E("a", b="c")) == "<a b='c' />"
    assert str(E("a", b="c", d=True)) == "<a b='c' d />"


def test_with_text():
    assert str(E("a")["hello world"]) == "<a>hello world</a>"
    assert str(E("a", b="c")["hello world"]) == "<a b='c'>hello world</a>"
    assert str(E("a", b="c", d=True)["hello world"]) == "<a b='c' d>hello world</a>"

    assert str(E("a")["hello ", "world"]) == "<a>hello world</a>"
    assert str(E("a", b="c")["hello ", "world"]) == "<a b='c'>hello world</a>"
    assert str(E("a", b="c", d=True)["hello ", "world"]) == "<a b='c' d>hello world</a>"


def test_nested():
    assert str(E("a")[E("b")["hello world"]]) == "<a><b>hello world</b></a>"
    assert str(E("a")[E("b", c="d")["hello world"]]) == "<a><b c='d'>hello world</b></a>"
    assert str(E("a")[E("b", c="d", e=True)["hello world"]]) == "<a><b c='d' e>hello world</b></a>"

    assert str(E("a")[E("b")["hello ", "world"]]) == "<a><b>hello world</b></a>"
    assert str(E("a")[E("b", c="d")["hello ", "world"]]) == "<a><b c='d'>hello world</b></a>"
    assert (
        str(E("a")[E("b", c="d", e=True)["hello ", "world"]])
        == "<a><b c='d' e>hello world</b></a>"
    )
