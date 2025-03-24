from app.domain.entities.bio import BioEntity
from app.infrastructure.repositories.base import AbstractRepository
from abc import ABC, abstractmethod


class BiosRepository(AbstractRepository[BioEntity], ABC):
    @abstractmethod
    async def get_by_user_oid(self, user_id: str) -> BioEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: BioEntity) -> BioEntity:
        raise NotImplementedError

    @abstractmethod
    async def get(self, oid: str) -> BioEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: BioEntity) -> BioEntity:
        raise NotImplementedError

    @abstractmethod
    async def list(self, start: int = 0, limit: int = 10) -> list[BioEntity]:
        raise NotImplementedError
