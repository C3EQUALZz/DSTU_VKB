from typing import TYPE_CHECKING, Final

from aiogram import Bot
from aiogram.types import BufferedInputFile
from typing_extensions import override

from compressor.application.common.ports.sender import FileForSendInfoDTO, Sender
from compressor.application.common.ports.storage import FileStorage, FileStorageDTO
from compressor.application.common.ports.user_query_gateway import UserQueryGateway
from compressor.application.errors.user import UserNotFoundError
from compressor.domain.users.values.user_id import UserID
from compressor.infrastructure.errors.file_storage import FileInStorageNotFoundError
from compressor.infrastructure.errors.sender import UserDoesntHaveTelegramAccountError
from compressor.setup.configs.telegram import TGConfig

if TYPE_CHECKING:
    from compressor.domain.users.entities.user import User


class TelegramSender(Sender):
    def __init__(
            self,
            tg_config: TGConfig,
            user_query_gateway: UserQueryGateway,
            file_storage: FileStorage,
            bot: Bot
    ) -> None:
        self._tg_config: Final[TGConfig] = tg_config
        self._user_query_gateway: Final[UserQueryGateway] = user_query_gateway
        self._file_storage: Final[FileStorage] = file_storage
        self._bot: Bot = bot

    @override
    async def send_file(self, user_id: UserID, file: FileForSendInfoDTO) -> None:
        user: User | None = await self._user_query_gateway.read_by_id(
            user_id=user_id,
        )
        msg: str

        if user is None:
            msg = f"User with id: {user_id} not found"
            raise UserNotFoundError(msg)

        file_from_storage: FileStorageDTO | None = await self._file_storage.read_by_id(file_id=file.file_id)

        if file_from_storage is None:
            msg = f"File with id: {file.file_id} not found"
            raise FileInStorageNotFoundError(msg)

        file_value_in_bytes: bytes = file_from_storage.data.getvalue()
        filename: str = str(file_from_storage.name)

        document: BufferedInputFile = BufferedInputFile(file_value_in_bytes, filename=filename)

        if user.telegram is None:
            msg = f"User with id: {user.id} does not have telegram account"
            raise UserDoesntHaveTelegramAccountError(msg)

        await self._bot.send_document(chat_id=user.telegram.id, document=document)
