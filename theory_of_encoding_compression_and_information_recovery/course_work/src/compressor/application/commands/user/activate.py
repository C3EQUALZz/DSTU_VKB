import logging
from dataclasses import dataclass
from typing import final, Final, cast
from uuid import UUID

from compressor.application.common.ports.transaction_manager import TransactionManager
from compressor.application.common.ports.user_command_gateway import UserCommandGateway
from compressor.application.errors.user import UserNotFoundError
from compressor.application.services.user.current_user_service import CurrentUserService
from compressor.domain.users.entities.user import User

from compressor.domain.users.services.authorization.permission import (
    CanManageRole,
    RoleManagementContext,
    CanManageSubordinate,
    UserManagementContext
)

from compressor.domain.users.services.authorization_service import AuthorizationService
from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.user_role import UserRole

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ActivateUserCommand:
    user_id: UUID


@final
class ActivateUserCommandHandler:
    """
    - Open to admins.
    - Restores a previously soft-deleted user.
    - Only super admins can activate other admins.
    """

    def __init__(
            self,
            current_user_service: CurrentUserService,
            user_command_gateway: UserCommandGateway,
            authorization_service: AuthorizationService,
            transaction_manager: TransactionManager,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._auth_service: Final[AuthorizationService] = authorization_service
        self._transaction_manager: Final[TransactionManager] = transaction_manager

    async def __call__(self, data: ActivateUserCommand) -> None:
        logger.info(
            "Activate user: started. User id: '%s'.",
            data.user_id,
        )

        current_user: User = await self._current_user_service.get_current_user()

        self._auth_service.authorize(
            CanManageRole(),
            context=RoleManagementContext(
                subject=current_user,
                target_role=UserRole.USER,
            ),
        )

        typed_user_id: UserID = cast(UserID, data.user_id)

        user: User | None = await self._user_command_gateway.read_by_id(
            typed_user_id,
        )

        if user is None:
            msg: str = "Can't find by id error"
            raise UserNotFoundError(msg)

        self._auth_service.authorize(
            CanManageSubordinate(),
            context=UserManagementContext(
                subject=current_user,
                target=user,
            ),
        )

        self._auth_service.toggle_user_activation(user, is_active=True)
        await self._transaction_manager.commit()

        logger.info(
            "Activate user: done. Username: '%s'.",
            user.username.value,
        )
