from collections import deque
from dataclasses import dataclass, field
from typing import Iterable

from cryptography_methods.domain.common.entities.base_entity import BaseEntity, OIDType
from cryptography_methods.domain.common.events import BaseDomainEvent


@dataclass
class BaseAggregateRoot(BaseEntity[OIDType]):
    _events: deque[BaseDomainEvent] = field(
        default_factory=deque,
        init=False,
        repr=False,
        hash=False,
        compare=False,
    )

    def register_event(self, event: BaseDomainEvent) -> None:
        self._events.append(event)

    def register_events(self, event: Iterable[BaseDomainEvent]) -> None:
        self._events.extend(event)

    def get_events(self) -> deque[BaseDomainEvent]:
        return self._events

    def clear_events(self) -> None:
        self._events.clear()

    def pull_events(self) -> deque[BaseDomainEvent]:
        events: deque[BaseDomainEvent] = self.get_events().copy()
        self.clear_events()
        return events
