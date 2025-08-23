from abc import abstractmethod
from typing import Protocol

from compressor.domain.users.entities.telegram_user import TelegramUser
from compressor.domain.users.values.telegram_user_id import TelegramID
from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.username import Username


class TelegramUserCommandGateway(Protocol):
    @abstractmethod
    async def add(self, user: TelegramUser) -> None:
        ...

    @abstractmethod
    async def read_by_id(self, user_id: UserID) -> TelegramUser | None:
        ...

    @abstractmethod
    async def read_by_telegram_user_id(self, telegram_id: TelegramID) -> TelegramUser | None:
        ...

    @abstractmethod
    async def read_by_username(self, username: Username) -> TelegramUser | None:
        ...
