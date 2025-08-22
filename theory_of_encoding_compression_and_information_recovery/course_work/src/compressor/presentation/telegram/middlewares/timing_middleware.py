import logging
import time
from typing import Final, Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing_extensions import override

logger: Final[logging.Logger] = logging.getLogger(__name__)


class TimingMiddleware(BaseMiddleware):
    @override
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        start_time: float = time.perf_counter()
        result: Any = await handler(event, data)
        end_time: float = time.perf_counter()
        logger.debug("Timing for processing is %s", end_time - start_time)
        return result