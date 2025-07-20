from pyx import E
from pyx.component import PatchType, diff


def test_change_text():
    assert diff(E("div")["aaa"], E("div")["bbb"]) == [(PatchType.CHANGE_TEXT, "bbb")]
