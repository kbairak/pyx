from collections.abc import Mapping

import pyx
from pyx import E
from pyx.node import Node


def test_literal():
    node = Node("hello world", 123)
    assert node == Node.from_values(parent=123, tag="LITERAL", value="hello world")


def test_fragment():
    node = Node(E()["hello world"], 123)

    expected = Node.from_values(
        parent=123,
        tag="",
        value={"children": Node.from_values(parent=None, tag="LITERAL", value="hello world")},
        props={"children": "hello world"},
    )
    assert isinstance(expected.value, Mapping)
    assert isinstance(expected.value["children"], Node)
    expected.value["children"].parent = node

    assert node == expected


def test_div():
    node = Node(E("div")["hello world"], 123)

    expected = Node.from_values(
        parent=123,
        tag="div",
        value={"children": Node.from_values(parent=None, tag="LITERAL", value="hello world")},
        props={"children": "hello world"},
    )
    assert isinstance(expected.value, Mapping)
    assert isinstance(expected.value["children"], Node)
    expected.value["children"].parent = node

    assert node == expected


def test_function_that_returns_div():
    def Main():
        return E("div")["hello world"]

    node = Node(E(Main), 123)

    expected = Node.from_values(
        parent=123,
        tag=Main,
        value=Node.from_values(
            parent=None,
            tag="div",
            value={"children": Node.from_values(parent=None, tag="LITERAL", value="hello world")},
            props={"children": "hello world"},
        ),
        props={},
        state=[],
    )
    assert isinstance(expected.value, Node)
    expected.value.parent = node
    assert isinstance(expected.value.value, Mapping)
    assert isinstance(expected.value.value["children"], Node)
    expected.value.value["children"].parent = node.value

    assert node == expected


def test_function_that_returns_literal():
    def Main():
        return "hello world"

    node = Node(E(Main), 123)

    expected = Node.from_values(
        parent=123,
        tag=Main,
        value=Node.from_values(parent=None, tag="LITERAL", value="hello world"),
        state=[],
    )
    assert isinstance(expected.value, Node)
    expected.value.parent = node

    assert node == expected


def test_function_with_state():
    def Main():
        msg, _ = pyx.use_state("hello world")
        return E("div")[msg]

    node = Node(E(Main), 123)

    expected = Node.from_values(
        parent=123,
        tag=Main,
        value=Node.from_values(
            parent=None,
            tag="div",
            value={"children": Node.from_values(parent=None, tag="LITERAL", value="hello world")},
            props={"children": "hello world"},
        ),
        state=[("hello world",)],
    )
    assert isinstance(expected.value, Node)
    expected.value.parent = node
    assert isinstance(expected.value.value, Mapping)
    assert isinstance(expected.value.value["children"], Node)
    expected.value.value["children"].parent = node.value

    assert node == expected


def test_function_with_state_and_literal():
    def Main():
        msg, _ = pyx.use_state("hello world")
        return msg

    node = Node(E(Main), 123)

    expected = Node.from_values(
        parent=123,
        tag=Main,
        value=Node.from_values(
            parent=None,
            tag="LITERAL",
            value="hello world",
        ),
        state=[("hello world",)],
    )
    assert isinstance(expected.value, Node)
    expected.value.parent = node

    assert node == expected


def test_nested():
    def Inner():
        return "hello world"

    def Outer():
        return E(Inner)

    node = Node(E(Outer), 123)

    expected = Node.from_values(
        parent=123,
        tag=Outer,
        value=Node.from_values(
            parent=None,
            tag=Inner,
            value=Node.from_values(
                parent=None,
                tag="LITERAL",
                value="hello world",
            ),
            state=[],
        ),
        state=[],
    )
    assert isinstance(expected.value, Node)
    expected.value.parent = node
    assert isinstance(expected.value.value, Node)
    expected.value.value.parent = node.value

    assert node == expected


def test_many_children():
    node = Node(
        E("a")[E("b")["bbb"], E("c")["ccc"]],
        123,
    )

    expected = Node.from_values(
        parent=123,
        tag="a",
        value={
            "children": [
                Node.from_values(
                    parent=None,
                    tag="b",
                    value={"children": Node.from_values(parent=None, tag="LITERAL", value="bbb")},
                    props={"children": "bbb"},
                ),
                Node.from_values(
                    parent=None,
                    tag="c",
                    value={"children": Node.from_values(parent=None, tag="LITERAL", value="ccc")},
                    props={"children": "ccc"},
                ),
            ]
        },
        props={"children": [E("b")["bbb"], E("c")["ccc"]]},
    )
    assert isinstance(expected.value, dict)
    assert isinstance(expected.value["children"], list)
    expected.value["children"][0].parent = node
    assert isinstance(node.value, dict)
    assert isinstance(node.value["children"], list)
    expected.value["children"][0].value["children"].parent = node.value["children"][0]
    expected.value["children"][1].parent = node
    expected.value["children"][1].value["children"].parent = node.value["children"][1]

    assert node == expected


def test_fragment_with_function_child():
    def Main():
        msg, _ = pyx.use_state("hello world")
        return msg

    node = Node(E()[E(Main)], 123)

    expected = Node.from_values(
        parent=123,
        tag="",
        value={
            "children": Node.from_values(
                parent=None,
                tag=Main,
                value=Node.from_values(parent=None, tag="LITERAL", value="hello world"),
                state=[("hello world",)],
            )
        },
        props={"children": E(Main)},
    )
    assert isinstance(expected.value, dict)
    assert isinstance(expected.value["children"], Node)
    expected.value["children"].parent = node
    assert isinstance(expected.value["children"].value, Node)
    assert isinstance(node.value, dict)
    expected.value["children"].value.parent = node.value["children"]

    assert node == expected
