import taskiq_aiogram
from taskiq_redis import ListQueueBroker

from app.settings.config import get_settings

broker = ListQueueBroker(str(get_settings().cache.url))

taskiq_aiogram.init(
    broker,
    # This is path to the dispatcher.
    "app.main:dp",
    # This is path to the bot instance.
    "app.main:bot",
    # You can specify more bots here.
)
