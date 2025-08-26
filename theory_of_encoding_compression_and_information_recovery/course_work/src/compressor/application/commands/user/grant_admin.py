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
class GrantAdminCommand:
    user_id: UUID


@final
class GrantAdminCommandHandler:
    """
    - Open to super admins.
    - Grants admin rights to a specified user.
    - Super admin rights can not be changed.
    """

    def __init__(
            self,
            current_user_service: CurrentUserService,
            user_command_gateway: UserCommandGateway,
            user_service: UserService,
            authorization_service: AuthorizationService,
            transaction_manager: TransactionManager,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._user_service: Final[UserService] = user_service
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._authorization_service: Final[AuthorizationService] = authorization_service

    async def __call__(self, data: GrantAdminCommand) -> None:
        """
        :raises AuthenticationError:
        :raises DataMapperError:
        :raises AuthorizationError:
        :raises DomainFieldError:
        :raises UserNotFoundByUsernameError:
        :raises RoleChangeNotPermittedError:
        """
        logger.info(
            "Grant admin: started. user id: '%s'.",
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

        typed_user_id: UserID = cast("UserID", data.user_id)

        user: User | None = await self._user_command_gateway.read_by_id(
            typed_user_id,
        )

        if user is None:
            msg: str = f"User with id: %{data.user_id} not found error"
            raise UserNotFoundError(msg)

        self._authorization_service.toggle_user_admin_role(user, is_admin=True)
        await self._transaction_manager.commit()

        logger.info("Grant admin: done. Username: '%s'.", user.username.value)
