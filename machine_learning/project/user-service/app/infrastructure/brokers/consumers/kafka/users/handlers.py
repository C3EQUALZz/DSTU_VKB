from typing import Final

from dishka import FromDishka
from faststream import Logger
from faststream.kafka import KafkaRouter, KafkaMessage

from app.infrastructure.brokers.consumers.kafka.users.schemas import UserStartsBotSchema
from app.logic.bootstrap import Bootstrap
from app.logic.events.telegram import UserStartTelegramEvent
from app.logic.message_bus import MessageBus
from app.settings.config import get_settings, Settings

router: Final[KafkaRouter] = KafkaRouter()
settings: Final[Settings] = get_settings()


@router.subscriber(
    settings.broker.user_telegram_id_from_start_bot_topic,
    group_id=settings.broker.user_telegram_id_from_start_bot_group_id,
    no_ack=True,
    description="Consumer for handling user starts bot",
)
async def handle_user_started_bot(
        msg: KafkaMessage,
        bootstrap: FromDishka[Bootstrap],
        logger: Logger,
        schemas: UserStartsBotSchema
) -> None:
    logger.info("Handling user starts bot")

    message_bus: MessageBus = await bootstrap.get_messagebus()
    await message_bus.handle(
        UserStartTelegramEvent(
            oid=schemas.event_id,
            user_id=schemas.user_id,
            telegram_id=schemas.telegram_id,
        )
    )

    await msg.ack()

    logger.info("Success for user starts bot")
