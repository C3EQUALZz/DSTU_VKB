from abc import abstractmethod
from collections.abc import Iterable
from typing import Protocol

from chat_service.domain.common.events import BaseDomainEvent


class EventBus(Protocol):
    @abstractmethod
    async def publish(self, events: Iterable[BaseDomainEvent]) -> None:
        raise NotImplementedError
