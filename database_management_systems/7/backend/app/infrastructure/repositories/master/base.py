from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.master import MasterEntity
from app.infrastructure.repositories.base import AbstractRepository


class MasterRepository(AbstractRepository[MasterEntity], ABC):
    """
    An interface for work with clients, that is used by clients unit of work.
    The main goal is that implementations of this interface can be easily replaced in clients unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_phone_number(self, number: str) -> Optional[MasterEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_full_name(self, name: str, surname: str, patronymic: str):
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: MasterEntity) -> MasterEntity:
        raise NotImplementedError

    @abstractmethod
    async def get(self, oid: str) -> Optional[MasterEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: MasterEntity) -> MasterEntity:
        raise NotImplementedError

    @abstractmethod
    async def list(self, start: int = 0, limit: int = 10) -> List[MasterEntity]:
        raise NotImplementedError
