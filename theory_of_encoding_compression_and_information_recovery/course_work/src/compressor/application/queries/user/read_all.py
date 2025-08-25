import logging
from dataclasses import dataclass
from typing import final, Final

from compressor.application.common.ports.user_query_gateway import UserQueryGateway
from compressor.application.common.query_params.pagination import Pagination
from compressor.application.common.query_params.sorting import SortingOrder
from compressor.application.common.query_params.user import UserListParams, UserListSorting
from compressor.application.common.views.users import UserView
from compressor.application.errors.query import SortingError
from compressor.application.services.user.current_user_service import CurrentUserService
from compressor.domain.users.entities.user import User
from compressor.domain.users.services.authorization.permission import CanManageRole, RoleManagementContext
from compressor.domain.users.services.authorization_service import AuthorizationService
from compressor.domain.users.values.user_role import UserRole

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadAllUsersQuery:
    limit: int
    offset: int
    sorting_field: str
    sorting_order: SortingOrder


@final
class ReadAllUsersQueryHandler:
    def __init__(
            self,
            current_user_service: CurrentUserService,
            user_query_gateway: UserQueryGateway,
            authorization_service: AuthorizationService,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._user_query_gateway: Final[UserQueryGateway] = user_query_gateway
        self._authorization_service: Final[AuthorizationService] = authorization_service

    async def __call__(self, data: ReadAllUsersQuery) -> list[UserView]:
        logger.info("Read all users started.")

        logger.info("Checking for current user...")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Current user detected: %s", current_user.id)

        logger.info("Authorizing user, user_id: %s...", current_user.id)

        self._authorization_service.authorize(
            CanManageRole(),
            context=RoleManagementContext(
                subject=current_user,
                target_role=UserRole.USER,
            ),
        )
        logger.info("Successfully authorized. User: %s", current_user.id)

        logger.debug("Retrieving list of users.")

        user_list_params: UserListParams = UserListParams(
            pagination=Pagination(
                limit=data.limit,
                offset=data.offset,
            ),
            sorting=UserListSorting(
                sorting_field=data.sorting_field,
                sorting_order=data.sorting_order,
            ),
        )

        users: list[User] | None = await self._user_query_gateway.read_all(
            user_list_params,
        )

        if users is None:
            logger.error(
                "Retrieving list of users failed: invalid sorting column '%s'.",
                data.sorting_field,
            )
            raise SortingError("Invalid sorting field.")

        response: list[UserView] = [
            UserView(
                first_name=user.username.value,
                role=user.role,
                language=user.language.value,
                telegram_id=None if user.telegram is None else user.telegram.id,
            )
            for user in users
        ]

        logger.info("Successfully retrieved list of users. Returning to user")

        return response
