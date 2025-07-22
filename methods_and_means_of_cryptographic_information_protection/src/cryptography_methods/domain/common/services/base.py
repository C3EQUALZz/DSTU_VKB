from collections import deque
from copy import copy
from dataclasses import dataclass, field
from typing import Iterable

from cryptography_methods.domain.common.events import BaseDomainEvent


@dataclass
class DomainService:
    _events: deque[BaseDomainEvent] = field(default_factory=deque)

    def _record_event(self, event: BaseDomainEvent) -> None:
        self._events.append(event)

    def _record_events(self, events: Iterable[BaseDomainEvent]) -> None:
        self._events.extend(events)

    def get_events(self) -> Iterable[BaseDomainEvent]:
        return self._events

    def clear_events(self) -> None:
        self._events.clear()

    def pull_events(self) -> Iterable[BaseDomainEvent]:
        events: Iterable[BaseDomainEvent] = copy(self.get_events())
        self.clear_events()
        return events
