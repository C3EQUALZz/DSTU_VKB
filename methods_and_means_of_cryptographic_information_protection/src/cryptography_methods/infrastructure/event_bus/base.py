from abc import abstractmethod
from typing import Protocol, Iterable

from cryptography_methods.domain.common.events import BaseDomainEvent


class EventBus(Protocol):
    @abstractmethod
    async def publish(self, events: Iterable[BaseDomainEvent]) -> None:
        ...
