from typing import Protocol
from abc import abstractmethod
from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.values.user_id import UserID


class UserCommandGateway(Protocol):
    @abstractmethod
    async def add(self, user: User) -> None:
        ...

    @abstractmethod
    async def read_by_id(self, user_id: UserID) -> User:
        ...

    async def read_all_by_social_media(self):
        ...
