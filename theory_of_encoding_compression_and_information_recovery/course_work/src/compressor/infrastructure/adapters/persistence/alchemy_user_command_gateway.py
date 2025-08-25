from typing import Final

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from compressor.application.common.ports.user_command_gateway import UserCommandGateway
from compressor.domain.users.entities.user import User
from compressor.domain.users.values.telegram_user_id import TelegramID
from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.username import Username


class SqlAlchemyUserCommandGateway(UserCommandGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    async def add(self, user: User) -> None:
        self._session.add(user)

    @override
    async def read_by_id(self, user_id: UserID) -> User | None:
        select_stmt: Select[tuple[User]] = select(
            User
        ).where(
            User.id == user_id  # type: ignore
        )

        user: User | None = (
            await self._session.execute(select_stmt)
        ).scalar_one_or_none()

        return user

    @override
    async def read_by_telegram_user_id(self, telegram_id: TelegramID) -> User | None:
        select_stmt: Select[tuple[User]] = select(
            User
        ).where(
            User.telegram.id == telegram_id  # type: ignore
        )

        user: User | None = (
            await self._session.execute(select_stmt)
        ).scalar_one_or_none()

        return user

    @override
    async def read_by_username(self, username: Username) -> User | None:
        select_stmt: Select[tuple[User]] = select(
            User
        ).where(
            User.username == username  # type: ignore
        )

        user: User | None = (
            await self._session.execute(select_stmt)
        ).scalar_one_or_none()

        return user
