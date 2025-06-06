from typing import Final

from dishka import FromDishka
from faststream import Logger
from faststream.kafka import KafkaRouter, KafkaMessage

from app.infrastructure.brokers.consumers.kafka.texts.schemas import MessageFromBrokerSchema
from app.logic.bootstrap import Bootstrap
from app.logic.events.texts import TextFromBrokerEvent
from app.logic.message_bus import MessageBus
from app.settings.configs.app import Settings, get_settings

settings: Final[Settings] = get_settings()
router: Final[KafkaRouter] = KafkaRouter()


@router.subscriber(
    settings.broker.text_to_chatbot_result_topic,
    group_id=settings.broker.text_telegram_group,
    auto_commit=False,
    description="Kafka message handler for getting rotated image"
)
async def handle_text_to_chatbot_result_topic(
        schemas: MessageFromBrokerSchema,
        msg: KafkaMessage,
        bootstrap: FromDishka[Bootstrap],
        logger: Logger,
) -> None:
    logger.info("Getting text, header: %s", msg.headers)

    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        TextFromBrokerEvent(
            content=schemas.content,
            chat_id=schemas.chat_id,
        )
    )

    await msg.ack()

    logger.info("Successfully handled text, header: %s", msg.headers)
