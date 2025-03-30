from abc import (
    ABC,
    abstractmethod,
)

from app.domain.entities.file_objects import CompressedFileObjectEntity
from app.infrastructure.repositories.base import AbstractRepository


class DatabaseDumpRepository(AbstractRepository[CompressedFileObjectEntity], ABC):
    @abstractmethod
    def add(self, model: CompressedFileObjectEntity) -> CompressedFileObjectEntity:
        raise NotImplementedError

    @abstractmethod
    def get(self, oid: str) -> CompressedFileObjectEntity | None:
        raise NotImplementedError

    @abstractmethod
    def update(self, oid: str, model: CompressedFileObjectEntity) -> CompressedFileObjectEntity:
        raise NotImplementedError

    @abstractmethod
    def list(self, start: int | None = None, limit: int | None = None) -> list[CompressedFileObjectEntity]:
        raise NotImplementedError
