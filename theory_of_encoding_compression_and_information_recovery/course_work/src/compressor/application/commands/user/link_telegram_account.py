import logging
from dataclasses import dataclass
from typing import Final, cast, final
from uuid import UUID

from compressor.application.common.ports.access_revoker import AccessRevoker
from compressor.application.common.ports.transaction_manager import TransactionManager
from compressor.application.common.ports.user_command_gateway import UserCommandGateway
from compressor.application.errors.user import (
    UserHasLinkedTelegramAccountBeforeError,
    UserIsBotError,
    UserNotFoundError,
)
from compressor.application.services.user.current_user_service import CurrentUserService
from compressor.domain.users.entities.telegram_user import TelegramUser
from compressor.domain.users.entities.user import User
from compressor.domain.users.services.authorization.composite import AnyOf
from compressor.domain.users.services.authorization.permission import (
    CanManageSelf,
    CanManageSubordinate,
    UserManagementContext,
)
from compressor.domain.users.services.authorization_service import AuthorizationService
from compressor.domain.users.services.telegram_service import TelegramService
from compressor.domain.users.values.telegram_user_id import TelegramID
from compressor.domain.users.values.user_first_name import UserFirstName
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
            current_user_service: CurrentUserService,
            authorization_service: AuthorizationService,
            access_revoker: AccessRevoker,
            user_command_gateway: UserCommandGateway,
            telegram_service: TelegramService,
            transaction_manager: TransactionManager,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._access_revoker: Final[AccessRevoker] = access_revoker
        self._authorization_service: Final[AuthorizationService] = authorization_service
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._telegram_service: Final[TelegramService] = telegram_service
        self._transaction_manager: Final[TransactionManager] = transaction_manager

    async def __call__(self, data: LinkTelegramAccountCommand) -> None:
        logger.info("Started link telegram account")

        logger.info("Detecting current user")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Current user detected, id: %s", current_user.id)

        typed_user_id: UserID = cast("UserID", data.user_id)

        logger.info("Searching user to link telegram by id: %s", data.user_id)
        user: User | None = await self._user_command_gateway.read_by_id(
            typed_user_id,
        )

        if user is None:
            msg: str = f"User with id: {data.user_id} does not exist."
            raise UserNotFoundError(msg)

        logger.info("User was successfully found with user id: %s", user.id)

        logger.info(
            "Started authorization for current user id: %s, user_id: %s",
            current_user.id,
            user.id
        )

        self._authorization_service.authorize(
            AnyOf(
                CanManageSelf(),
                CanManageSubordinate(),
            ),
            context=UserManagementContext(
                subject=current_user,
                target=user,
            ),
        )

        logger.info("User was successfully authorized")

        if user.telegram is not None:
            msg: str = f"User with id {user.id} has already linked telegram account."
            raise UserHasLinkedTelegramAccountBeforeError(msg)

        if data.is_bot is True:
            await self._access_revoker.remove_all_user_access(user_id=typed_user_id)
            msg: str = "User was permanently banned."
            raise UserIsBotError(msg)

        logger.info("Started link telegram account for user with id: %s", user.id)

        new_telegram_account: TelegramUser = self._telegram_service.create(
            telegram_id=cast("TelegramID", data.telegram_id),
            first_name=cast("UserFirstName", data.first_name),
            username=data.username,
            last_name=data.last_name,
            is_premium=data.is_premium,
            is_bot=data.is_bot,
        )

        user.telegram = new_telegram_account
        await self._transaction_manager.commit()

        logger.info(
            "Finished link telegram account for user with id: %s",
            new_telegram_account.id
        )
