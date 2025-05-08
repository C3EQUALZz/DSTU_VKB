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


@router.subscriber(settings.broker.user_create_topic)
async def handle_create_user_from_telegram(
        schemas: UserSchemaEvent,
        msg: KafkaMessage,
        bootstrap: FromDishka[Bootstrap],
        logger: Logger,
) -> None:
    logger.info("Getting info from topic: %s", settings.broker.user_create_topic)

    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        CreateUserCommand(
            oid=schemas.event_id,
            first_name=schemas.first_name,
            role=schemas.role,
            telegram_id=schemas.telegram_id,
        )
    )

    await msg.ack()

    logger.info("Successfully got info from topic: %s", settings.broker.user_create_topic)



@router.subscriber(settings.broker.user_delete_topic)
async def handle_delete_user_from_telegram() -> None:
    ...


@router.subscriber(settings.broker.user_update_topic)
async def handle_update_user_from_telegram() -> None:
    ...
