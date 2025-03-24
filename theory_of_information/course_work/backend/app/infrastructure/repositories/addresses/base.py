from app.domain.entities.address import AddressEntity
from abc import ABC, abstractmethod
from app.infrastructure.repositories.base import AbstractRepository


class AddressRepository(AbstractRepository[AddressEntity], ABC):
    ...
