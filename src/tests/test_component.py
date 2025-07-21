from pyx import E
from pyx.component import PatchType, diff


def test_change_text():
    assert diff(E("div")["aaa"], E("div")["bbb"]) == [(PatchType.CHANGE_TEXT, "bbb")]


def test_replace_none_with_new_child():
    assert diff(E()[None], E()["hello world"]) == [(PatchType.REPLACE_CHILD, 0, "hello world")]
    assert diff(E()["aaa", None], E()["aaa", "bbb"]) == [(PatchType.REPLACE_CHILD, 1, "bbb")]
    assert diff(E()["aaa", None, "ccc"], E()["aaa", "bbb", "ccc"]) == [
        (PatchType.REPLACE_CHILD, 1, "bbb")
    ]


def test_set_prop():
    assert diff(E(""), E("", a="b")) == [(PatchType.SET_PROP, "a", "b")]
    assert diff(E("", a="b"), E("", a="c")) == [(PatchType.SET_PROP, "a", "c")]
    assert diff(E("", a="b"), E("", a="b")) == []


def test_remove_prop():
    assert diff(E("", a="b"), E("")) == [(PatchType.REMOVE_PROP, "a", None)]
    assert diff(E("", a="b", c="d"), E("", c="d")) == [(PatchType.REMOVE_PROP, "a", None)]
    assert diff(E("", a="b", c="d"), E("", a="b", c="d")) == []
