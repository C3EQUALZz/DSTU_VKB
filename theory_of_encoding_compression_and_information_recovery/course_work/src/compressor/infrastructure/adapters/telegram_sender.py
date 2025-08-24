from aiogram import Bot
from typing_extensions import override
from typing import Final
from compressor.application.common.ports.sender import Sender, FileForSendInfoDTO
from compressor.application.common.ports.user.telegram_user_query_gateway import TelegramUserQueryGateway
from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.entities.telegram_user import TelegramUser

class TelegramSender(Sender):
    def __init__(self, bot: Bot, telegram_query_gateway: TelegramUserQueryGateway) -> None:
        self._bot: Final[Bot] = bot
        self._telegram_user_query_gateway: Final[TelegramUserQueryGateway] = telegram_query_gateway

    @override
    async def send_file(self, user_id: UserID, file: FileForSendInfoDTO) -> None:
        telegram_user: TelegramUser = await self._telegram_user_query_gateway.read_by_id(
            user_id=user_id,
        )

        await self._bot.send_document(
            chat_id=telegram_user.id,
            document=
        )
