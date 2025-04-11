from abc import (
    ABC,
    abstractmethod,
)

from app.domain.entities.user import UserEntity
from app.infrastructure.repositories.base import AbstractRepository


class UsersRepository(AbstractRepository[UserEntity], ABC):
    """
    An interface for work with User, that is used by UserUnitOfWork.
    The main goal is that implementations of this interface can be easily replaced in UserUnitOfWork
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_fullname(self, surname: str, name: str, patronymic: str) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None:
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
    async def list(self, start: int = 0, limit: int = 10) -> list[UserEntity]:
        raise NotImplementedError
