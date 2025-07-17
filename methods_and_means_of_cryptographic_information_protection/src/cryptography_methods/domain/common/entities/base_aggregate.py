from collections import deque
from typing import Iterable, Final

from cryptography_methods.domain.common.entities.base_entity import BaseEntity, OIDType
from cryptography_methods.domain.common.events import BaseDomainEvent


class BaseAggregateRoot(BaseEntity[OIDType]):
    def __init__(self, id: OIDType) -> None:
        super().__init__(id)
        self._events: Final[deque[BaseDomainEvent]] = deque()

    def _register_event(self, event: BaseDomainEvent) -> None:
        self._events.append(event)

    def _register_events(self, event: Iterable[BaseDomainEvent]) -> None:
        self._events.extend(event)

    def get_events(self) -> deque[BaseDomainEvent]:
        return self._events

    def clear_events(self) -> None:
        self._events.clear()

    def pull_events(self) -> deque[BaseDomainEvent]:
        events: deque[BaseDomainEvent] = self.get_events().copy()
        self.clear_events()
        return events
