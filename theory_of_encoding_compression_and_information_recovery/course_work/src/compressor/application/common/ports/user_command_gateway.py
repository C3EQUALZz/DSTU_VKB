from abc import abstractmethod
from typing import Protocol

from compressor.domain.users.entities.user import User
from compressor.domain.users.values.telegram_user_id import TelegramID
from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.username import Username


class UserCommandGateway(Protocol):
    @abstractmethod
    async def add(self, user: User) -> None:
        ...

    @abstractmethod
    async def read_by_id(self, user_id: UserID) -> User | None:
        ...

    @abstractmethod
    async def read_by_telegram_user_id(self, telegram_id: TelegramID) -> User | None:
        ...

    @abstractmethod
    async def read_by_username(self, username: Username) -> User | None:
        ...
