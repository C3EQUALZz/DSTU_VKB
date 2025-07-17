from typing import Protocol
from abc import abstractmethod
from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.values.telegram_id import TelegramID
from cryptography_methods.domain.user.values.user_id import UserID


class UserCommandGateway(Protocol):
    @abstractmethod
    async def add(self, user: User) -> None:
        ...

    @abstractmethod
    async def read_by_id(
            self,
            user_id: UserID,
            for_update: bool = False
    ) -> User | None:
        ...

    @abstractmethod
    async def read_by_telegram_id(self, tg_id: TelegramID) -> User | None:
        ...
