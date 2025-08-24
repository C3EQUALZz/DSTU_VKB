import asyncio
from typing import Final

from aiogram import Bot
from aiogram.types import BufferedInputFile
from typing_extensions import override

from compressor.application.common.ports.sender import Sender, FileForSendInfoDTO
from compressor.application.common.ports.storage import FileStorage, FileStorageDTO
from compressor.application.common.ports.telegram_user_query_gateway import TelegramUserQueryGateway
from compressor.domain.users.entities.telegram_user import TelegramUser
from compressor.domain.users.values.user_id import UserID


class TelegramSender(Sender):
    def __init__(
            self,
            bot: Bot,
            telegram_query_gateway: TelegramUserQueryGateway,
            file_storage: FileStorage,
    ) -> None:
        self._bot: Final[Bot] = bot
        self._telegram_user_query_gateway: Final[TelegramUserQueryGateway] = telegram_query_gateway
        self._file_storage: Final[FileStorage] = file_storage

    @override
    async def send_file(self, user_id: UserID, file: FileForSendInfoDTO) -> None:
        telegram_user: TelegramUser = await self._telegram_user_query_gateway.read_by_id(
            user_id=user_id,
        )

        file_from_storage: FileStorageDTO = await self._file_storage.read_by_id(file_id=file.file_id)

        file_value_in_bytes: bytes = file_from_storage.data.getvalue()
        filename: str = str(file_from_storage.path)

        document: BufferedInputFile = BufferedInputFile(file_value_in_bytes, filename=filename)

        await self._bot.send_document(
            chat_id=telegram_user.id,
            document=document,
        )
