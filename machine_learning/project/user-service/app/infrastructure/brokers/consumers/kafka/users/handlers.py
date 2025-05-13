from typing import Final

from dishka import FromDishka
from faststream.kafka import KafkaRouter, KafkaMessage
from faststream import Logger

from app.infrastructure.brokers.consumers.kafka.users.schemas import UserSchemaEvent
from app.logic.bootstrap import Bootstrap
from app.logic.commands.users import CreateUserCommand
from app.logic.message_bus import MessageBus
from app.settings.config import get_settings, Settings

router: Final[KafkaRouter] = KafkaRouter()
settings: Final[Settings] = get_settings()