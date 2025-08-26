from collections.abc import Callable
from typing import Final, TypeVar

from dishka.integrations.aiogram import CONTAINER_NAME
from dishka.integrations.base import wrap_injection

T = TypeVar("T")

DATA_PARAMETER_POSITION: Final[int] = 3  # self 0, handler 1 , event 2, <data 3>


def inject(func: Callable[..., T]) -> Callable[..., T]:
    return wrap_injection(
        func=func,
        container_getter=lambda args, _kwargs: args[DATA_PARAMETER_POSITION][CONTAINER_NAME],
        is_async=True,
    )
