from sqlalchemy import Select, select

from cryptography_methods.application.common.ports.user.command_gateway import UserCommandGateway
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override
from typing import Final
from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.values.telegram_id import TelegramID
from cryptography_methods.domain.user.values.user_id import UserID


class SQLAlchemyUserCommandGateway(UserCommandGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    async def add(self, user: User) -> None:
        self._session.add(user)

    @override
    async def read_by_id(
            self,
            user_id: UserID,
            for_update: bool = False
    ) -> User | None:
        select_stmt: Select[tuple[User]] = select(User).where(User.id == user_id)  # type: ignore

        if for_update:
            select_stmt.with_for_update()

        user: User | None = (
            await self._session.execute(select_stmt)
        ).scalar_one_or_none()

        return user

    @override
    async def read_by_telegram_id(self, tg_id: TelegramID) -> User | None:
        ...
