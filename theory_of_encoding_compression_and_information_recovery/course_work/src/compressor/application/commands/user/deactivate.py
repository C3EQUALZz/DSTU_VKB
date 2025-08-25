import logging
from dataclasses import dataclass
from typing import final, Final, cast
from uuid import UUID

from compressor.application.common.ports.access_revoker import AccessRevoker
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
from compressor.domain.users.services.user_service import UserService
from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.user_role import UserRole

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class DeactivateUserCommand:
    user_id: UUID


@final
class DeactivateUserCommandHandler:
    """
    - Open to admins.
    - Soft-deletes an existing user, making that user inactive.
    - Also deletes the user's sessions.
    - Only super admins can deactivate other admins.
    - Super admins cannot be soft-deleted.
    """

    def __init__(
            self,
            current_user_service: CurrentUserService,
            user_command_gateway: UserCommandGateway,
            user_service: UserService,
            authorization_service: AuthorizationService,
            transaction_manager: TransactionManager,
            access_revoker: AccessRevoker,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._user_service: Final[UserService] = user_service
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._access_revoker: Final[AccessRevoker] = access_revoker
        self._authorization_service: Final[AuthorizationService] = authorization_service

    async def __call__(self, data: DeactivateUserCommand) -> None:
        logger.info(
            "Deactivate user: started. user id: '%s'.",
            data.user_id,
        )

        current_user: User = await self._current_user_service.get_current_user()

        self._authorization_service.authorize(
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

        self._authorization_service.authorize(
            CanManageSubordinate(),
            context=UserManagementContext(
                subject=current_user,
                target=user,
            ),
        )

        self._authorization_service.toggle_user_activation(user, is_active=True)
        await self._access_revoker.remove_all_user_access(user_id=user.id)
        await self._transaction_manager.commit()

        logger.info(
            "Deactivate user: done. User id: '%s'.",
            user.id,
        )
