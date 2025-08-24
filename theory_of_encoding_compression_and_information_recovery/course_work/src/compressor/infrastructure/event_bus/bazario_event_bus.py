import asyncio
import logging
from asyncio import Task
from collections.abc import Iterable
from typing import Final

from bazario.asyncio import Publisher
from typing_extensions import override

from compressor.domain.common.events import BaseDomainEvent
from compressor.infrastructure.event_bus.base import EventBus

logger: Final[logging.Logger] = logging.getLogger(__name__)


class BazarioEventBus(EventBus):
    def __init__(self, publisher: Publisher) -> None:
        self._publisher: Final[Publisher] = publisher

    @override
    async def publish(self, events: Iterable[BaseDomainEvent]) -> None:
        logger.info("Publishing events....")
        background_tasks: set[Task] = set()

        for event in events:
            task: Task = asyncio.create_task(self._publisher.publish(event))
            logger.info("Published event from event bus: %s", event)
            background_tasks.add(task)
            task.add_done_callback(background_tasks.discard)
