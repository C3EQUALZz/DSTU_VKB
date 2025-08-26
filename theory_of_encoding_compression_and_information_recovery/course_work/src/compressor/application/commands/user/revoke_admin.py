import logging
from dataclasses import dataclass
from typing import Final, cast, final
from uuid import UUID

from compressor.application.common.ports.transaction_manager import TransactionManager
from compressor.application.common.ports.user_command_gateway import UserCommandGateway
from compressor.application.errors.user import UserNotFoundError
from compressor.application.services.user.current_user_service import CurrentUserService
from compressor.domain.users.entities.user import User
from compressor.domain.users.services.authorization.permission import (
    CanManageRole,
    RoleManagementContext,
)
from compressor.domain.users.services.authorization_service import AuthorizationService
from compressor.domain.users.services.user_service import UserService
from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.user_role import UserRole

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RevokeAdminCommand:
    user_id: UUID


@final
class RevokeAdminCommandHandler:
    """
    - Open to super admins.
    - Revokes admin rights from a specified user.
    - Super admin rights can not be changed
    """

    def __init__(
            self,
            current_user_service: CurrentUserService,
            user_command_gateway: UserCommandGateway,
            user_service: UserService,
            transaction_manager: TransactionManager,
            authorization_service: AuthorizationService,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._user_service: Final[UserService] = user_service
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._authorization_service: Final[AuthorizationService] = authorization_service

    async def __call__(self, data: RevokeAdminCommand) -> None:
        """
        :raises AuthenticationError:
        :raises DataMapperError:
        :raises AuthorizationError:
        :raises DomainFieldError:
        :raises UserNotFoundByUsernameError:
        :raises RoleChangeNotPermittedError:
        """
        logger.info(
            "Revoke admin: started. User id: '%s'.",
            data.user_id,
        )

        current_user: User = await self._current_user_service.get_current_user()

        self._authorization_service.authorize(
            CanManageRole(),
            context=RoleManagementContext(
                subject=current_user,
                target_role=UserRole.ADMIN,
            ),
        )

        user_id: UserID = cast("UserID", data.user_id)

        user: User | None = await self._user_command_gateway.read_by_id(
            user_id=user_id,
        )

        if user is None:
            msg: str = "User with id '%s' not found"
            raise UserNotFoundError(msg)

        self._authorization_service.toggle_user_admin_role(user, is_admin=False)
        await self._transaction_manager.commit()

        logger.info(
            "Revoke admin: done. Username: '%s'.",
            user.username.value,
        )
