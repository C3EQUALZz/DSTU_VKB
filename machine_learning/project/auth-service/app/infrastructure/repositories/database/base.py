import builtins
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar, overload

from app.domain.entities.base import BaseEntity

BaseEntityType = TypeVar("BaseEntityType", bound=BaseEntity)


class AbstractRepository(ABC, Generic[BaseEntityType]):
    """
    Interface for any repository, which would be used for work with domain model, according DDD.

    Main purpose is to encapsulate internal logic that is associated with the use of one or another data
    storage scheme, for example, ORM.
    """

    @abstractmethod
    async def add(self, model: BaseEntityType) -> BaseEntityType:
        raise NotImplementedError

    @abstractmethod
    async def get(self, oid: str) -> Optional[BaseEntityType]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: BaseEntityType) -> BaseEntityType:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, oid: str) -> None:
        raise NotImplementedError

    @overload
    async def list(self) -> builtins.list[BaseEntityType]:
        ...

    @overload
    async def list(self, start: int, limit: int) -> builtins.list[BaseEntityType]:
        ...

    @abstractmethod
    async def list(self, start: int | None = None, limit: int | None = None) -> builtins.list[BaseEntityType]:
        raise NotImplementedError


