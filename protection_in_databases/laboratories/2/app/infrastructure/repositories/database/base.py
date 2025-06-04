from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar, overload

from app.domain.entities.base import BaseEntity

BaseEntityType = TypeVar("BaseEntityType", bound=BaseEntity)


class AbstractRepository(ABC, Generic[BaseEntityType]):
    """
    Interface for any repository, which would be used for work with domain model, according DDD.

    Main purpose is to encapsulate internal logic that is associated with the use of one or another data
    storage scheme, for example, ORM.
    """

    @abstractmethod
    def add(self, model: BaseEntityType) -> BaseEntityType:
        raise NotImplementedError

    @abstractmethod
    def get(self, oid: str) -> Optional[BaseEntityType]:
        raise NotImplementedError

    @abstractmethod
    def update(self, oid: str, model: BaseEntityType) -> BaseEntityType:
        raise NotImplementedError

    @abstractmethod
    def delete(self, oid: str) -> None:
        raise NotImplementedError

    @overload
    def list(self, start: None, limit: None) -> List[BaseEntityType]:
        ...

    @overload
    def list(self, start: int, limit: int) -> List[BaseEntityType]:
        ...

    @abstractmethod
    def list(self, start: int | None = None, limit: int | None = None) -> List[BaseEntityType]:
        raise NotImplementedError


