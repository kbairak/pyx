from collections.abc import Callable
from dataclasses import dataclass

from .component import active_component


def use_state[T](default: T = None) -> tuple[T, Callable[[T], None]]:
    component = active_component["current"]
    if component is None:
        raise RuntimeError("`use_state` must be called within a component function")
    if component.pointer is None:
        component.state.append(default)
        index = len(component.state) - 1
        return component.state[-1], lambda x: component.set_state(index, x)
    else:
        result = (
            component.state[component.pointer],
            lambda x: component.set_state(component.pointer, x),
        )
        component.pointer += 1
        return result


@dataclass
class Ref[T]:
    current: T | None = None


def use_ref[T](default: T = None) -> Ref[T]:
    ref, _ = use_state(Ref(default))
    return ref


def use_effect(compare_list):
    def decorator(func):
        component = active_component["current"]
        if component is None:
            raise RuntimeError("`use_effect` must be called within a component function")
        if component.pointer is None:
            callback = func()
            component.state.append((compare_list, callback))
        else:
            prev_compare_list, prev_callback = component.state[component.pointer]
            if prev_compare_list != compare_list:
                if prev_callback is not None:
                    prev_callback()
                callback = func()
                component.state[component.pointer] = (compare_list, callback)
            component.pointer += 1

    return decorator
