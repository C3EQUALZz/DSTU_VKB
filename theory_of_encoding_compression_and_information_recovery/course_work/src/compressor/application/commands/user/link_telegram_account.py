import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, cast, final
from uuid import UUID

from compressor.application.common.ports.access_revoker import AccessRevoker
from compressor.application.common.ports.transaction_manager import TransactionManager
from compressor.application.common.ports.user_command_gateway import UserCommandGateway
from compressor.application.errors.user import (
    UserHasLinkedTelegramAccountBeforeError,
    UserIsBotError,
    UserNotFoundError,
)
from compressor.domain.users.services.telegram_service import TelegramService
from compressor.domain.users.values.user_first_name import UserFirstName
from compressor.domain.users.values.username import Username

if TYPE_CHECKING:
    from compressor.domain.users.entities.telegram_user import TelegramUser
    from compressor.domain.users.entities.user import User
    from compressor.domain.users.values.telegram_user_id import TelegramID
    from compressor.domain.users.values.user_id import UserID

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class LinkTelegramAccountCommand:
    user_id: UUID
    telegram_id: int
    first_name: str
    username: str | None
    last_name: str | None
    is_premium: bool | None
    is_bot: bool | None


@final
class LinkTelegramAccountCommandHandler:
    def __init__(
        self,
        access_revoker: AccessRevoker,
        user_command_gateway: UserCommandGateway,
        telegram_service: TelegramService,
        transaction_manager: TransactionManager,
    ) -> None:
        self._access_revoker: Final[AccessRevoker] = access_revoker
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._telegram_service: Final[TelegramService] = telegram_service
        self._transaction_manager: Final[TransactionManager] = transaction_manager

    async def __call__(self, data: LinkTelegramAccountCommand) -> None:
        logger.info("Started link telegram account")

        typed_user_id: UserID = cast("UserID", data.user_id)

        logger.info("Searching user to link telegram by id: %s", data.user_id)
        user: User | None = await self._user_command_gateway.read_by_id(
            typed_user_id,
        )

        msg: str

        if user is None:
            msg = f"User with id: {data.user_id} does not exist."
            raise UserNotFoundError(msg)

        logger.info("User was successfully found with user id: %s", user.id)

        if user.telegram is not None:
            msg = f"User with id {user.id} has already linked telegram account."
            raise UserHasLinkedTelegramAccountBeforeError(msg)

        if data.is_bot is True:
            await self._access_revoker.remove_all_user_access(user_id=typed_user_id)
            msg = "User was permanently banned."
            raise UserIsBotError(msg)

        logger.info("Started link telegram account for user with id: %s", user.id)

        new_telegram_account: TelegramUser = self._telegram_service.create(
            telegram_id=cast("TelegramID", data.telegram_id),
            first_name=UserFirstName(data.first_name),
            username=Username(data.username) if data.username is not None else Username(data.first_name),
            last_name=data.last_name,
            is_premium=data.is_premium if data.is_premium is not None else False,
            is_bot=data.is_bot if data.is_bot is not None else False,
        )

        user.telegram = new_telegram_account
        await self._transaction_manager.commit()

        logger.info("Finished link telegram account for user with id: %s", new_telegram_account.id)
