from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class UUIDProvider(Protocol):
    @abstractmethod
    def __call__(self) -> UUID:
        raise NotImplementedError
