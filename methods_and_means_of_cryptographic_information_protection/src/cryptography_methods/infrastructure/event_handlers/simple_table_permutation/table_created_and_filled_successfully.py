from aiogram import Bot
from typing import Final
from typing_extensions import override

from cryptography_methods.domain.cipher_table.events import TableCreatedAndFilledSuccessfullyEvent
from cryptography_methods.infrastructure.event_handlers.base import EventHandler


class SendBotTableCreatedAndFilledSuccessfullyEventHandler(EventHandler):
    def __init__(self, bot: Bot) -> None:
        self._bot: Final[Bot] = bot

    @override
    async def __call__(self, event: TableCreatedAndFilledSuccessfullyEvent) -> None:
        await self._bot.send_message(

        )
