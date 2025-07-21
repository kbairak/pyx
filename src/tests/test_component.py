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
