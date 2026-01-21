from collections import deque
from collections.abc import Iterable
from copy import copy

from vulnfinder.domain.common.events import BaseDomainEvent


class BaseDomainService:
    def __init__(self) -> None:
        self._events: deque[BaseDomainEvent] = deque()

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
