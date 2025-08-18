import asyncio
from collections.abc import Callable
from dataclasses import dataclass

from pyx.utils import defer

from .node import active


def use_state[T](default: T = None) -> tuple[T, Callable[[T | Callable[[T], T]], None]]:
    node = active.node
    if node is None:
        raise RuntimeError("`use_state` must be called within a component function")
    assert isinstance(node.state, list)
    if active.pointer is None:
        index = len(node.state)
        node.state.append((default,))
    else:
        index = active.pointer
        active.pointer += 1

    def _setter(value_or_setter_func: T | Callable[[T], T]) -> None:
        assert isinstance(node.state, list)
        (prev_value,) = node.state[index]
        value = (
            value_or_setter_func(prev_value)
            if callable(value_or_setter_func)
            else value_or_setter_func
        )
        node.set_state(index, value)

    (prev_value,) = node.state[index]
    return prev_value, _setter


@dataclass
class Ref[T]:
    current: T | None = None


def use_ref[T](default: T = None) -> Ref[T]:
    ref, _ = use_state(Ref(default))
    return ref


def use_effect(compare_list) -> Callable[[Callable[[], None | Callable[[], None]]], None]:
    def decorator(func: Callable[[], None | Callable[[], None]]):
        node = active.node
        if node is None:
            raise RuntimeError("`use_effect` must be called within a component function")
        assert isinstance(node.state, list)
        if active.pointer is None:
            pointer = len(node.state)
            node.state.append((compare_list, None))

            @defer
            async def _():
                callback = func()
                assert isinstance(node.state, list)
                node.state[pointer] = (compare_list, callback)

        else:
            pointer = active.pointer
            active.pointer += 1

            @defer
            async def _():
                assert isinstance(node.state, list)
                prev_compare_list, prev_callback = node.state[pointer]
                if prev_compare_list != compare_list:
                    if prev_callback is not None:
                        prev_callback()
                    callback = func()
                    node.state[pointer] = (compare_list, callback)

    return decorator


def use_task(compare_list):
    def decorator(func):
        task: Ref[asyncio.Task | None] = use_ref()

        @use_effect(compare_list)
        def _():
            task.current = asyncio.create_task(func())

            def _callback():
                assert task.current is not None
                task.current.cancel()

            return _callback

    return decorator
