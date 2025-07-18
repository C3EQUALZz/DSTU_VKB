import asyncio
from asyncio import Task
from typing import Iterable

from bazario.asyncio import Publisher
from typing_extensions import override

from cryptography_methods.domain.common.events import BaseDomainEvent
from cryptography_methods.infrastructure.event_bus.base import EventBus


class BazarioEventBus(EventBus):
    def __init__(self, publisher: Publisher) -> None:
        self._publisher: Publisher = publisher

    @override
    async def publish(self, events: Iterable[BaseDomainEvent]) -> None:
        background_tasks: set[Task] = set()

        for event in events:
            task: Task = asyncio.create_task(self._publisher.publish(event))
            background_tasks.add(task)
            task.add_done_callback(background_tasks.discard)
