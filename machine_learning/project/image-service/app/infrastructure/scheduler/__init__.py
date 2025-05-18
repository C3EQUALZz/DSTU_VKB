import logging
from typing import Final

from dishka import AsyncContainer
from dishka.integrations.faststream import setup_dishka as setup_dishka_faststream
from dishka.integrations.taskiq import setup_dishka as setup_taskiq_dishka
from faststream import FastStream
from faststream.kafka import KafkaBroker
from taskiq import TaskiqEvents, TaskiqState, SmartRetryMiddleware
from taskiq_redis import ListQueueBroker

from app.logic.container import get_container
from app.settings.configs.app import get_settings, Settings
from app.settings.configs.enums import TasksMiddlewareDefaultConfig

settings: Final[Settings] = get_settings()
logger: Final[logging.Logger] = logging.getLogger(__name__)
scheduler: Final[ListQueueBroker] = ListQueueBroker(str(get_settings().cache.url)).with_middlewares(
    SmartRetryMiddleware(
        default_retry_count=TasksMiddlewareDefaultConfig.DEFAULT_RETRY_COUNT.value,
        default_delay=TasksMiddlewareDefaultConfig.DEFAULT_RETRY_DELAY.value,
        use_jitter=TasksMiddlewareDefaultConfig.USE_JITTER.value,
        use_delay_exponent=TasksMiddlewareDefaultConfig.USE_DELAY_EXPONENT.value,
        max_delay_exponent=TasksMiddlewareDefaultConfig.MAX_DELAY_COMPONENT.value,
    ),
)


@scheduler.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    container: AsyncContainer = get_container()
    faststream_broker: KafkaBroker = await container.get(KafkaBroker)
    setup_taskiq_dishka(container=container, broker=scheduler)
    setup_dishka_faststream(container=container, app=FastStream(faststream_broker, logger=logger), auto_inject=True)
    await faststream_broker.start()
    logger.info("taskiq startup event ends...")
