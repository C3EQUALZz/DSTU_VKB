import logging

from typing import Final

from dishka import AsyncContainer
from dishka.integrations.taskiq import setup_dishka as setup_taskiq_dishka
from dishka.integrations.faststream import setup_dishka as setup_dishka_faststream
from faststream import FastStream
from faststream.kafka import KafkaBroker
from taskiq import TaskiqEvents, TaskiqState
from taskiq_redis import ListQueueBroker

from app.logic.container import get_container
from app.settings.configs.app import get_settings

logger: Final[logging.Logger] = logging.getLogger(__name__)
scheduler: Final[ListQueueBroker] = ListQueueBroker(str(get_settings().cache.url))


@scheduler.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    container: AsyncContainer = get_container()
    faststream_broker: KafkaBroker = await container.get(KafkaBroker)
    setup_taskiq_dishka(container=container, broker=scheduler)
    setup_dishka_faststream(container=container, app=FastStream(faststream_broker, logger=logger), auto_inject=True)
    await faststream_broker.start()
    logger.info("taskiq startup event ends...")

