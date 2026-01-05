from abc import abstractmethod
from typing import Protocol

from chat_service.domain.user.entities.user import User
from chat_service.domain.user.values.user_id import UserID


class UserCommandGateway(Protocol):
    @abstractmethod
    async def add(self, user: User) -> None:
        ...

    @abstractmethod
    async def read_by_id(self, user_id: UserID) -> User:
        ...

    @abstractmethod
    async def delete_by_id(self, user_id: UserID) -> None:
        ...
