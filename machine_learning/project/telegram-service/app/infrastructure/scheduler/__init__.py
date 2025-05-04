from typing import Final

import taskiq_aiogram
from dishka.integrations.taskiq import setup_dishka as setup_taskiq_dishka
from taskiq_redis import ListQueueBroker

from app.logic.container import get_container
from app.settings.configs.app import get_settings

scheduler: Final[ListQueueBroker] = ListQueueBroker(str(get_settings().cache.url))

setup_taskiq_dishka(container=get_container(), broker=scheduler)

taskiq_aiogram.init(
    scheduler,
    "app.main:dp",
    "app.main:bot",
)
