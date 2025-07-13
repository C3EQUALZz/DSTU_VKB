from abc import abstractmethod
from typing import Protocol

from cryptography_methods.domain.common.events import BaseDomainEvent


class EventHandler(Protocol):
    @abstractmethod
    async def __call__(self, event: BaseDomainEvent) -> None:
        ...
