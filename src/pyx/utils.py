import asyncio
from asyncio import Task
from collections.abc import Callable, Coroutine


def defer(func: Callable[[], Coroutine[None, None, None]]) -> Task:
    """
    >>> @defer
    ... async def _():
    ...     ...

    Should be equivalent to:

    >>> async def _():
    ...     ...
    >>> create_task(_())

    """

    return asyncio.create_task(func())
