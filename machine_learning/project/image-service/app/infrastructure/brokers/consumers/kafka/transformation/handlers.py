from typing import Final

from dishka import FromDishka
from faststream import Logger
from faststream.kafka import KafkaRouter, KafkaMessage

from app.infrastructure.brokers.consumers.kafka.transformation.schemas import CropImageAndSendToChatSchema, \
    RotateImageAndSendToChatSchema
from app.logic.bootstrap import Bootstrap
from app.logic.events.transform import CropImageAndSendToChatEvent, RotateImageAndSendToChatEvent
from app.logic.message_bus import MessageBus
from app.settings.configs.app import Settings, get_settings

settings: Final[Settings] = get_settings()
router: Final[KafkaRouter] = KafkaRouter()


@router.subscriber(
    settings.broker.image_crop_topic,
    group_id=settings.broker.image_crop_group,
    auto_commit=False,
    description="Kafka message handler for cropping image"
)
async def handle_image_crop_topic(
        schemas: CropImageAndSendToChatSchema,
        msg: KafkaMessage,
        bootstrap: FromDishka[Bootstrap],
        logger: Logger
) -> None:
    logger.info("Handling cropping image event from telegram")
    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        CropImageAndSendToChatEvent(
            data=schemas.image.data,
            name=schemas.image.name,
            old_width=schemas.image.width,
            old_height=schemas.image.height,
            new_width=schemas.new_width,
            new_height=schemas.new_height,
            chat_id=schemas.chat_id,
        )
    )

    msg.ack()

    logger.info("Successfully handled cropping image event from telegram")


@router.subscriber(
    settings.broker.image_rotate_topic,
    group_id=settings.broker.image_rotate_group,
    auto_commit=False,
    description="Kafka message handler for rotating images"
)
async def handle_image_rotate_topic(
        schemas: RotateImageAndSendToChatSchema,
        msg: KafkaMessage,
        bootstrap: FromDishka[Bootstrap],
        logger: Logger
) -> None:
    logger.info("Handling rotating image event from telegram")

    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        RotateImageAndSendToChatEvent(
            data=schemas.image.data,
            name=schemas.image.name,
            width=schemas.image.width,
            height=schemas.image.height,
            chat_id=schemas.chat_id,
            angle=schemas.angle,
        )
    )

    msg.ack()

    logger.info("Successfully handled rotating image event from telegram")