from collections.abc import Callable, Sequence
from copy import deepcopy
from typing import Self


class E:
    def __init__(self, tag: Callable | str = "", *children, **props):
        self.tag = tag
        self.children = list(children)
        self.props = props

    def __call__(self, *children, **props) -> Self:
        return self.__class__(self.tag, *self.children, *children, **self.props, **props)

    def __getitem__(self, index) -> Self:
        if isinstance(index, Sequence) and not isinstance(index, str):
            return self(*index)
        else:
            return self(index)

    def __copy__(self) -> Self:
        return deepcopy(self)

    def __str__(self) -> str:
        tag_str = self.tag.__name__ if callable(self.tag) else str(self.tag)

        if self.props:
            props_list = []
            for key, value in self.props.items():
                if value is True:
                    props_list.append(key)
                else:
                    props_list.append(f"{key}={value!r}")
            props_str = " " + " ".join(props_list)
        else:
            props_str = ""

        if self.children:
            return (
                f"<{tag_str}{props_str}>"
                f"{''.join(str(child) for child in self.children)}"
                f"</{tag_str}>"
            )
        else:
            return f"<{tag_str}{props_str} />"
