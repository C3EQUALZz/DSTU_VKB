from aiogram import BaseMiddleware
from typing import Final, Callable, Dict, Any, Awaitable
from typing_extensions import override
from aiogram.types import TelegramObject


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, *, limit: int = 5, interval: int = 10) -> None:
        self._limit: Final[int] = limit
        self._interval: Final[int] = interval

    @override
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> None:
        ...
