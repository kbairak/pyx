import asyncio
from asyncio import Task
from collections.abc import Callable, Coroutine


def defer(func: Callable[[], Coroutine[None, None, None]]) -> Task:
    """
    >>> @defer
    ... async def task():
    ...     ...

    Should be equivalent to:

    >>> async def _():
    ...     ...
    >>> task = create_task(_())

    """

    return asyncio.create_task(func())


def singleton[T](cls: Callable[[], T]):
    """
    >>> @singleton
    ... class foo:
    ...     ...

    Should be equivalent to:

    >>> class foo:
    ...     ...
    >>> foo = foo()
    """

    return cls()
