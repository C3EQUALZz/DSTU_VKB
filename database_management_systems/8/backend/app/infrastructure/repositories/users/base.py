from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
    Optional,
)

from app.domain.entities.user import UserEntity
from app.infrastructure.repositories.base import AbstractRepository


class UsersRepository(AbstractRepository[UserEntity], ABC):
    """
    An interface for work with users, that is used by users unit of work.
    The main goal is that implementations of this interface can be easily replaced in users unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: UserEntity) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    async def get(self, oid: str) -> Optional[UserEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: UserEntity) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[UserEntity]:
        raise NotImplementedError
