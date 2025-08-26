import time
from collections.abc import Awaitable, Callable
from typing import Any, Final, cast

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing_extensions import override


class StaleMessageMiddleware(BaseMiddleware):
    def __init__(self, *, max_age: float = 120) -> None:  # 2 минуты
        self._max_age: Final[float] = max_age

    @override
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        message: Message = cast("Message", data.get("message"))

        if message:
            message_age: float = time.time() - message.date.timestamp()
            if message_age > self._max_age:
                await message.answer("⚠️ Это сообщение устарело. Пожалуйста, отправьте команду заново.")
                return None

        return await handler(event, data)
