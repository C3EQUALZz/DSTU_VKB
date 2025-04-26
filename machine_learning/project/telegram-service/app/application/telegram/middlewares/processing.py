import logging
from logging import Logger
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Final,
)

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram_i18n import I18nContext

from app.application.telegram.fsms.app import AppState


logger: Final[Logger] = logging.getLogger(__name__)


class ProcessingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:

        state = data.get("state")

        logger.debug("Processing state %s", state)

        if await state.get_state() == AppState.PROCESSING:

            logger.debug("User spamming, sending stop flood message")

            i18n: I18nContext = data.get("i18n")
            await event.answer(i18n.get("stop-flood"))
            return

        return await handler(event, data)
