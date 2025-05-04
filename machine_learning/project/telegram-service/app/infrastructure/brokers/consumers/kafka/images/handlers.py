from typing import Final

from dishka import FromDishka
from faststream import Logger
from faststream.kafka import KafkaRouter, KafkaMessage

from app.infrastructure.brokers.consumers.kafka.images.schemas import ImageWithTelegramChatId
from app.logic.bootstrap import Bootstrap
from app.logic.events.images import ConvertedImageFromBrokerEvent
from app.logic.message_bus import MessageBus
from app.settings.configs.app import Settings, get_settings

settings: Final[Settings] = get_settings()
router: Final[KafkaRouter] = KafkaRouter()


@router.subscriber(
    settings.broker.image_rotate_result_topic,
    settings.broker.image_crop_result_topic,
    settings.broker.image_grayscale_to_color_result_topic,
    settings.broker.image_color_to_grayscale_result_topic,
    settings.broker.image_style_result_topic,
    group_id=settings.broker.image_telegram_group,
    auto_commit=False,
    description="Kafka message handler for getting rotated image"
)
async def handle_image_rotate_result_topic(
        schemas: ImageWithTelegramChatId,
        msg: KafkaMessage,
        bootstrap: FromDishka[Bootstrap],
        logger: Logger,
) -> None:
    logger.info("Getting image, header: %s", msg.headers)

    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        ConvertedImageFromBrokerEvent(
            data=schemas.data,
            name=schemas.name,
            width=schemas.width,
            height=schemas.height,
            chat_id=schemas.chat_id,
        )
    )

    msg.ack()

    logger.info("Successfully handled image, header: %s", msg.headers)