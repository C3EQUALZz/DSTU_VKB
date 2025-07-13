from abc import ABC
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass, field

from cryptography_methods.domain.common.events import BaseDomainEvent


@dataclass
class BaseService(ABC):
    """
    Each Domain Service must inherit from this class.
    With this class, we can add different events from business logic.
    For example, user created -> event for another microservice.
    """
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
