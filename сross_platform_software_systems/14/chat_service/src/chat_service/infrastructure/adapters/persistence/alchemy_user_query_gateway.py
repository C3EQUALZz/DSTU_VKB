from typing import Final

from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from chat_service.application.common.ports.user.user_query_gateway import UserQueryGateway
from chat_service.application.common.query_params.user_filters import UserListParams
from chat_service.domain.user.entities.user import User
from chat_service.domain.user.values.user_id import UserID
from chat_service.infrastructure.adapters.persistence.constants import DB_QUERY_FAILED
from chat_service.infrastructure.errors.transaction_manager import RepoError


class SqlAlchemyUserQueryGateway(UserQueryGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    async def read_user_by_id(self, user_id: UserID) -> User | None:
        select_stmt: Select[tuple[User]] = select(User).where(User.id == user_id)  # type: ignore

        try:
            user: User | None = (await self._session.execute(select_stmt)).scalar_one_or_none()
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error
        else:
            return user

    @override
    async def read_all_users(self, user_list_params: UserListParams) -> list[User] | None:
        raise NotImplementedError
