from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.domain.entities.base import BaseEntity
from botocore.client import BaseClient

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
    async def get(self, oid: str) -> BaseEntityType | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: BaseEntityType) -> BaseEntityType:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, oid: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list(self, start: int | None = None, limit: int | None = None) -> list[BaseEntityType]:
        raise NotImplementedError


class S3AbstractRepository(AbstractRepository, ABC):
    def __init__(
        self,
        client: BaseClient,
        bucket_path: str,
        bucket_name: str,
    ) -> None:
        self._client = client
        self._bucket_path = bucket_path
        self._bucket_name = bucket_name
