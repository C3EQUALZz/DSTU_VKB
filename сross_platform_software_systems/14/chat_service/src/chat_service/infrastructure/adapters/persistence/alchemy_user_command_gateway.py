from typing import Final

from sqlalchemy import select, Select, Delete, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from chat_service.application.common.ports.user.user_command_gateway import UserCommandGateway
from chat_service.domain.user.entities.user import User
from chat_service.domain.user.values.user_id import UserID
from chat_service.infrastructure.adapters.persistence.constants import DB_QUERY_FAILED
from chat_service.infrastructure.errors.transaction_manager import RepoError


class SqlAlchemyUserCommandGateway(UserCommandGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    async def add(self, user: User) -> None:
        try:
            self._session.add(user)
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error

    @override
    async def read_by_id(self, user_id: UserID) -> User:
        select_stmt: Select[tuple[User]] = select(User).where(User.id == user_id)  # type: ignore

        try:
            user: User | None = (await self._session.execute(select_stmt)).scalar_one_or_none()
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error
        else:
            return user

    @override
    async def delete_by_id(self, user_id: UserID) -> None:
        delete_stm: Delete = delete(User).where(User.id == user_id)  # type: ignore

        try:
            await self._session.execute(delete_stm)
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error

    @override
    async def update(self, user: User) -> None:
        update_stmt = (
            update(User)
            .where(User.id == user.id)  # type: ignore
            .values(
                name=user.name,
                role=user.role,
                is_active=user.is_active,
                updated_at=user.updated_at,
            )
        )

        try:
            await self._session.execute(update_stmt)
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error
