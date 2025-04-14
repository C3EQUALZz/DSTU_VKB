import taskiq_aiogram
from dishka.integrations.taskiq import setup_dishka as setup_taskiq_dishka
from taskiq_redis import ListQueueBroker

from app.logic.container import get_container
from app.settings.config import get_settings

broker = ListQueueBroker(str(get_settings().cache.url))

taskiq_aiogram.init(
    broker,
    "app.main:dp",
    "app.main:bot",
)

setup_taskiq_dishka(container=get_container(), broker=broker)
