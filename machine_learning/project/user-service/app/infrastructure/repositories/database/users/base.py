from abc import ABC, abstractmethod

from app.domain.entities.user import UserEntity
from app.infrastructure.repositories.database.base import AbstractRepository


class UsersRepository(AbstractRepository[UserEntity], ABC):
    """
    An interface for work with User, that is used by UserUnitOfWork.
    The main goal is that implementations of this interface can be easily replaced in UserUnitOfWork
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_all_by_name(self, name: str, start: int | None = None, limit: int | None = None) -> list[UserEntity]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: UserEntity) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    async def get(self, oid: str) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: UserEntity) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    async def list(self, start: int | None = None, limit: int | None = None) -> list[UserEntity]:
        raise NotImplementedError
