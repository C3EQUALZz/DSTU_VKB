import logging
from dataclasses import dataclass
from typing import Final, final, cast

from compressor.application.common.ports.telegram_user_command_gateway import TelegramUserCommandGateway
from compressor.application.common.ports.telegram_user_query_gateway import TelegramUserQueryGateway
from compressor.application.common.ports.transaction_manager import TransactionManager
from compressor.application.common.views.register_via_telegram import RegisterViaTelegramView
from compressor.application.errors.user import UserNotFoundError
from compressor.domain.users.entities.telegram_user import TelegramUser
from compressor.domain.users.services.telegram_service import TelegramService
from compressor.domain.users.values.telegram_user_id import TelegramID
from compressor.domain.users.values.user_raw_password import UserRawPassword
from compressor.domain.users.values.username import Username

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class RegisterViaTelegramCommand:
    telegram_id: int
    username: str
    password: str


@final
class RegisterViaTelegramCommandHandler:
    def __init__(
            self,
            telegram_command_gateway: TelegramUserCommandGateway,
            telegram_query_gateway: TelegramUserQueryGateway,
            transaction_manager: TransactionManager,
            telegram_service: TelegramService,
    ) -> None:
        self._telegram_command_gateway: Final[TelegramUserCommandGateway] = telegram_command_gateway
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._telegram_service: Final[TelegramService] = telegram_service
        self._telegram_query_gateway: Final[TelegramUserQueryGateway] = telegram_query_gateway

    async def __call__(self, data: RegisterViaTelegramCommand) -> RegisterViaTelegramView:
        if await self._telegram_query_gateway.read_by_telegram_id(
                telegram_user_id=cast(TelegramID, data.telegram_id)
        ):
            msg: str = "User with telegram_id {} not found".format(data.telegram_id)
            raise UserNotFoundError(msg)

        new_telegram_user: TelegramUser = self._telegram_service.create(
            telegram_id=cast(TelegramID, data.telegram_id),
            username=Username(data.username),
            raw_password=UserRawPassword(data.password)
        )

        await self._telegram_command_gateway.add(user=new_telegram_user)
        await self._transaction_manager.flush()
        await self._transaction_manager.commit()

        return RegisterViaTelegramView(
            telegram_id=new_telegram_user.id,
            user_id=new_telegram_user.user.id,
            name=new_telegram_user.telegram_username.value
        )
