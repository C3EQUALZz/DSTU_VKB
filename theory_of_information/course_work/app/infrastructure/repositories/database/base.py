from abc import (
    ABC,
    abstractmethod,
)

from app.domain.entities.file_objects import CompressedFileObject
from app.infrastructure.repositories.base import AbstractRepository


class DatabaseDumpRepository(AbstractRepository[CompressedFileObject], ABC):
    @abstractmethod
    def add(self, model: CompressedFileObject) -> CompressedFileObject:
        raise NotImplementedError

    @abstractmethod
    def get(self, oid: str) -> CompressedFileObject | None:
        raise NotImplementedError

    @abstractmethod
    def update(self, oid: str, model: CompressedFileObject) -> CompressedFileObject:
        raise NotImplementedError

    @abstractmethod
    def list(self, start: int | None = None, limit: int | None = None) -> list[CompressedFileObject]:
        raise NotImplementedError
