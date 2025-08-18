from collections.abc import Callable, Sequence
from typing import Self


class E:
    def __init__(self, tag: Callable | str = "", **props):
        self.tag = tag
        self.props = props

    def __getitem__(self, index) -> Self:
        if "children" in self.props:
            raise ValueError("Cannot add children to an existing element")
        result = self.__class__(self.tag, **self.props)
        if isinstance(index, tuple):
            index = list(index)
        result.props["children"] = index
        return result

    def __str__(self) -> str:
        tag_str = self.tag.__name__ if callable(self.tag) else str(self.tag)

        props = dict(self.props)
        children = props.pop("children", None)

        if props:
            props_list = []
            for key, value in props.items():
                if value is True:
                    props_list.append(key)
                else:
                    props_list.append(f"{key}={value!r}")
            props_str = " " + " ".join(props_list)
        else:
            props_str = ""

        if children:
            if isinstance(children, Sequence) and not isinstance(children, str):
                children_str = "".join(str(child) for child in children)
            else:
                children_str = str(children)
            return f"<{tag_str}{props_str}>{children_str}</{tag_str}>"
        else:
            return f"<{tag_str}{props_str} />"

    def __eq__(self, other):
        return self.tag == other.tag and self.props == other.props
