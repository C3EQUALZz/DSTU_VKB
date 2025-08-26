from typing import Final

from aiogram import Bot
from aiogram.types import BufferedInputFile
from typing_extensions import override

from compressor.application.common.ports.sender import Sender, FileForSendInfoDTO
from compressor.application.common.ports.storage import FileStorage, FileStorageDTO
from compressor.application.common.ports.user_query_gateway import UserQueryGateway
from compressor.domain.users.entities.user import User
from compressor.domain.users.values.user_id import UserID
from compressor.infrastructure.errors.sender import UserDoesntHaveTelegramAccountError
from compressor.setup.configs.telegram import TGConfig


class TelegramSender(Sender):
    def __init__(
            self,
            tg_config: TGConfig,
            user_query_gateway: UserQueryGateway,
            file_storage: FileStorage,
    ) -> None:
        self._tg_config: Final[TGConfig] = tg_config
        self._user_query_gateway: Final[UserQueryGateway] = user_query_gateway
        self._file_storage: Final[FileStorage] = file_storage

    @override
    async def send_file(self, user_id: UserID, file: FileForSendInfoDTO) -> None:
        user: User = await self._user_query_gateway.read_by_id(
            user_id=user_id,
        )

        file_from_storage: FileStorageDTO = await self._file_storage.read_by_id(file_id=file.file_id)

        file_value_in_bytes: bytes = file_from_storage.data.getvalue()
        filename: str = str(file_from_storage.name)

        document: BufferedInputFile = BufferedInputFile(file_value_in_bytes, filename=filename)

        if user.telegram is None:
            msg: str = f"User with id: {user.id} does not have telegram account"
            raise UserDoesntHaveTelegramAccountError(msg)

        async with Bot(token=self._tg_config.admin_bot_token) as bot:
            await bot.send_document(chat_id=user.telegram.id, document=document)

