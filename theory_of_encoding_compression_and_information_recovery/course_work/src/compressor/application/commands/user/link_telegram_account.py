import logging
from dataclasses import dataclass
from typing import final, Final, cast
from uuid import UUID

from compressor.application.common.ports.access_revoker import AccessRevoker
from compressor.application.common.ports.user_command_gateway import UserCommandGateway
from compressor.application.errors.user import UserNotFoundError
from compressor.application.services.user.current_user_service import CurrentUserService
from compressor.domain.users.entities.telegram_user import TelegramUser
from compressor.domain.users.entities.user import User
from compressor.domain.users.services.authorization.composite import AnyOf
from compressor.domain.users.services.authorization.permission import (
    CanManageSelf,
    CanManageSubordinate,
    UserManagementContext
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
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._access_revoker: Final[AccessRevoker] = access_revoker
        self._authorization_service: Final[AuthorizationService] = authorization_service
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._telegram_service: Final[TelegramService] = telegram_service

    async def __call__(self, data: LinkTelegramAccountCommand) -> None:
        logger.info("Started link telegram account")

        current_user: User = await self._current_user_service.get_current_user()

        typed_user_id: UserID = cast(UserID, data.user_id)

        user: User | None = await self._user_command_gateway.read_by_id(
            typed_user_id,
        )

        if user is None:
            msg: str = f"User with id: {data.user_id} does not exist."
            raise UserNotFoundError(msg)

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

        if data.is_bot is True:
            await self._access_revoker.remove_all_user_access(user_id=typed_user_id)
            raise ...

        new_telegram_account: TelegramUser = self._telegram_service.create(
            telegram_id=cast(TelegramID, data.telegram_id),
            first_name=cast(UserFirstName, data.first_name),
            username=data.username,
            last_name=data.last_name,
            is_premium=data.is_premium,
            is_bot=data.is_bot,
        )


