from typing import Final

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from compressor.application.common.ports.user.telegram_user_command_gateway import TelegramUserCommandGateway
from compressor.domain.users.entities.telegram_user import TelegramUser
from compressor.domain.users.values.telegram_user_id import TelegramID
from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.username import Username


class SqlAlchemyTelegramUserCommandGateway(TelegramUserCommandGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    async def add(self, user: TelegramUser) -> None:
        self._session.add(user)

    @override
    async def read_by_id(self, user_id: UserID) -> TelegramUser | None:
        select_stmt: Select[tuple[TelegramUser]] = select(
            TelegramUser
        ).where(
            TelegramUser.user.id == user_id  # type: ignore
        )

        user: TelegramUser | None = (
            await self._session.execute(select_stmt)
        ).scalar_one_or_none()

        return user

    @override
    async def read_by_telegram_user_id(self, telegram_id: TelegramID) -> TelegramUser | None:
        select_stmt: Select[tuple[TelegramUser]] = select(
            TelegramUser
        ).where(
            TelegramUser.id == telegram_id  # type: ignore
        )

        user: TelegramUser | None = (
            await self._session.execute(select_stmt)
        ).scalar_one_or_none()

        return user

    @override
    async def read_by_username(self, username: Username) -> TelegramUser | None:
        select_stmt: Select[tuple[TelegramUser]] = select(
            TelegramUser
        ).where(
            TelegramUser.telegram_username == username  # type: ignore
        )

        user: TelegramUser | None = (
            await self._session.execute(select_stmt)
        ).scalar_one_or_none()

        return user
