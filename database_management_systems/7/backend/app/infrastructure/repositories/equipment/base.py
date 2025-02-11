from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
    Optional,
)

from app.domain.entities.equipment import EquipmentEntity
from app.infrastructure.repositories.base import AbstractRepository


class EquipmentRepository(AbstractRepository[EquipmentEntity], ABC):
    """
    An interface for work with equipment, that is used by equipment unit of work.
    The main goal is that implementations of this interface can be easily replaced in equipment unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_name_and_model(self, name: str, model: str) -> Optional[EquipmentEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_serial_number(self, serial_number: str) -> Optional[EquipmentEntity]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: EquipmentEntity) -> EquipmentEntity:
        raise NotImplementedError

    @abstractmethod
    async def get(self, oid: str) -> Optional[EquipmentEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: EquipmentEntity) -> EquipmentEntity:
        raise NotImplementedError

    @abstractmethod
    async def list(self, start: int = 0, limit: int = 10) -> List[EquipmentEntity]:
        raise NotImplementedError