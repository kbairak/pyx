import asyncio
from collections.abc import Callable
from dataclasses import dataclass

from pyx.utils import defer

from .component import active_component


def use_state[T](default: T = None) -> tuple[T, Callable[[T | Callable[[T], T]], None]]:
    component = active_component["current"]
    if component is None:
        raise RuntimeError("`use_state` must be called within a component function")
    if component.pointer is None:
        component.state.append((default,))
        index = len(component.state) - 1
    else:
        component.pointer += 1
        index = component.pointer - 1

    def _setter(value_or_setter_func: T | Callable[[T], T]) -> None:
        (prev_value,) = component.state[index]
        value = (
            value_or_setter_func(prev_value)
            if callable(value_or_setter_func)
            else value_or_setter_func
        )
        component.set_state(index, value)

    (prev_value,) = component.state[index]
    return prev_value, _setter


@dataclass
class Ref[T]:
    current: T | None = None


def use_ref[T](default: T = None) -> Ref[T]:
    ref, _ = use_state(Ref(default))
    return ref


def use_effect(compare_list) -> Callable[[Callable[[], None | Callable[[], None]]], None]:
    def decorator(func: Callable[[], None | Callable[[], None]]):
        component = active_component["current"]
        if component is None:
            raise RuntimeError("`use_effect` must be called within a component function")
        if component.pointer is None:
            pointer = len(component.state)
            component.state.append((compare_list, None))

            @defer
            async def _():
                component.state[pointer] = (compare_list, func())

        else:
            pointer = component.pointer

            @defer
            async def _():
                prev_compare_list, prev_callback = component.state[pointer]
                if prev_compare_list != compare_list:
                    if prev_callback is not None:
                        prev_callback()
                    component.state[pointer] = (compare_list, func())

            component.pointer += 1

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
