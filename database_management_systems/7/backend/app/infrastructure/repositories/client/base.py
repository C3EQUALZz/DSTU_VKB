from app.domain.entities.client import ClientEntity
from abc import ABC, abstractmethod
from typing import Optional, List
from app.infrastructure.repositories.base import AbstractRepository


class ClientRepository(AbstractRepository[ClientEntity], ABC):
    """
    An interface for work with clients, that is used by clients unit of work.
    The main goal is that implementations of this interface can be easily replaced in clients unit of work
    using dependency injection without disrupting its functionality.
    """

    # async def get_by_full_name(self, name: str, surname: str, patronomyc: str):

    @abstractmethod
    async def add(self, model: ClientEntity) -> ClientEntity:
        raise NotImplementedError

    @abstractmethod
    async def get(self, oid: str) -> Optional[ClientEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: ClientEntity) -> ClientEntity:
        raise NotImplementedError

    @abstractmethod
    async def list(self, start: int = 0, limit: int = 10) -> List[ClientEntity]:
        raise NotImplementedError

