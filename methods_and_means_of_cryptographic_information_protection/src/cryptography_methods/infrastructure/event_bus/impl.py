import asyncio
from collections import defaultdict
from typing import Iterable, Mapping

from typing_extensions import override

from cryptography_methods.domain.common.events import BaseDomainEvent
from cryptography_methods.infrastructure.event_bus.base import EventBus
from cryptography_methods.infrastructure.event_handlers.base import EventHandler


class ForwardEventBus(EventBus):
    def __init__(self) -> None:
        self._events_map: Mapping[type[BaseDomainEvent], list[EventHandler]] = defaultdict(list)

    def add_listener(self, event_type: type[BaseDomainEvent], listener: EventHandler) -> None:
        self._events_map[event_type].append(listener)

    def add_listeners(self, event_type: type[BaseDomainEvent], listeners: Iterable[EventHandler]) -> None:
        self._events_map[event_type].extend(listeners)

    def remove_listener(self, event_type: type[BaseDomainEvent], listener: EventHandler) -> None:
        self._events_map[event_type].remove(listener)

    def remove_listeners(self, event_type: type[BaseDomainEvent]) -> None:
        self._events_map[event_type].clear()
        del self._events_map[event_type]

    @override
    async def publish(self, events: Iterable[BaseDomainEvent]) -> None:
        for event in events:
            listeners: list[EventHandler] = self._events_map[type(event)]
            for listener in listeners:
                asyncio.create_task(listener(event))
