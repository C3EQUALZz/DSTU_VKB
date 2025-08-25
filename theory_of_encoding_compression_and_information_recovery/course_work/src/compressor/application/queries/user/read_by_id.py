import logging
from dataclasses import dataclass
from typing import cast
from typing import final, Final
from uuid import UUID

from compressor.application.common.ports.user_query_gateway import UserQueryGateway
from compressor.application.common.views.users import UserView
from compressor.application.services.user.current_user_service import CurrentUserService
from compressor.domain.users.entities.user import User
from compressor.domain.users.services.authorization.permission import CanManageRole, RoleManagementContext
from compressor.domain.users.services.authorization_service import AuthorizationService
from compressor.domain.users.values.telegram_user_id import TelegramID
from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.user_role import UserRole

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadUserByIDQuery:
    user_id: UUID


@final
class ReadUserByIDQueryHandler:
    def __init__(
            self,
            user_query_gateway: UserQueryGateway,
            current_user_service: CurrentUserService,
            authorization_service: AuthorizationService,
    ) -> None:
        self._user_query_gateway: Final[UserQueryGateway] = user_query_gateway
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._authorization_service: Final[AuthorizationService] = authorization_service

    async def __call__(self, data: ReadUserByIDQuery) -> UserView:
        logger.info("Read user by id started, user_id: %s", data.user_id)

        logger.info("Trying to ger current user")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Got current user, current user_id: %s", current_user.id)

        logger.info("Authorizing user, user_id: %s...", current_user.id)

        self._authorization_service.authorize(
            CanManageRole(),
            context=RoleManagementContext(
                subject=current_user,
                target_role=UserRole.USER,
            ),
        )
        logger.info("User successfully authorized, user_id: %s", current_user.id)

        typed_user_id: UserID = cast(UserID, data.user_id)

        logger.info("Trying to get user by id for admin: %s", data.user_id)
        user: User = await self._user_query_gateway.read_by_id(typed_user_id)

        telegram_id: None | TelegramID = None if user.telegram is None else user.telegram.id

        response: UserView = UserView(
            first_name=user.username.value,
            role=user.role,
            language=user.language.value,
            telegram_id=telegram_id,
        )

        logger.info("User successfully retrieved, user_id: %s", user.id)

        return response
