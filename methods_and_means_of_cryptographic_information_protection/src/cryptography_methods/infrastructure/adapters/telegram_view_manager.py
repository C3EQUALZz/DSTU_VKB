from typing import Iterable

from typing_extensions import override
from aiogram import Bot
from cryptography_methods.application.common.view_manager import ViewManager
from cryptography_methods.domain.user.values.user_id import UserID
from cryptography_methods.setup.settings import TelegramConfig


class TelegramViewManager(ViewManager):
    def __init__(self, tg_settings: TelegramConfig) -> None:
        self._tg_settings = tg_settings

    @override
    async def send_message_to_user(
            self,
            user_id: UserID,
            message: str
    ) -> None:
        async with Bot(token=self._tg_settings.token) as bot:
            await bot.send_message()

    @override
    async def send_table_to_user(
            self,
            user_id: UserID,
            table: Iterable[Iterable[str]],
            headers: Iterable[str] | None = None,
    ) -> None:
        ...

    @override
    async def send_greeting_to_user(
            self,
            user_id: UserID,
    ) -> None:
        ...
