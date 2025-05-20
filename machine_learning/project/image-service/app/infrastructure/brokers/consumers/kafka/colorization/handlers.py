from typing import Final

from dishka import FromDishka
from faststream import Logger
from faststream.kafka import KafkaRouter, KafkaMessage

from app.infrastructure.brokers.consumers.kafka.colorization.schemas import ConvertColorImageSchema, StylizeImageSchema
from app.logic.bootstrap import Bootstrap
from app.logic.events.colorization import StylizeAndSendToChatEvent, ConvertGrayScaleToColorAndSendToChatEvent, \
    ConvertColorToGrayScaleAndSendToChatEvent, ConvertImageInversionAndSendToChatEvent
from app.logic.message_bus import MessageBus
from app.settings.configs.app import Settings, get_settings

settings: Final[Settings] = get_settings()
router: Final[KafkaRouter] = KafkaRouter()


@router.subscriber(
    settings.broker.image_style_topic,
    group_id=settings.broker.image_style_group,
    no_ack=True,
    description="Kafka message handler for style image"
)
async def handle_image_style_topic(
        schemas: StylizeImageSchema,
        msg: KafkaMessage,
        bootstrap: FromDishka[Bootstrap],
        logger: Logger,
) -> None:
    logger.info("handling style image event from telegram")

    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        StylizeAndSendToChatEvent(
            original_image_data=schemas.original_image.data,
            original_width=schemas.original_image.width,
            original_height=schemas.original_image.height,
            original_name=schemas.original_image.name,
            style_image_data=schemas.style_image.data,
            style_width=schemas.style_image.width,
            style_height=schemas.style_image.height,
            style_name=schemas.style_image.name,
            chat_id=schemas.chat_id,
        )
    )

    await msg.ack()

    logger.info("successfully handled color image event from telegram")


@router.subscriber(
    settings.broker.image_grayscale_to_color_topic,
    group_id=settings.broker.image_grayscale_to_color_group,
    no_ack=True,
    description="Kafka message handler for grayscale image from color"
)
async def handle_image_grayscale_to_color_topic(
        schemas: ConvertColorImageSchema,
        msg: KafkaMessage,
        bootstrap: FromDishka[Bootstrap],
        logger: Logger
) -> None:
    logger.info("handling grayscale image event from telegram")

    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        ConvertGrayScaleToColorAndSendToChatEvent(
            data=schemas.image.data,
            width=schemas.image.width,
            height=schemas.image.height,
            chat_id=schemas.chat_id,
            name=schemas.image.name,
        )
    )

    await msg.ack()

    logger.info("successfully handled grayscale image event from telegram")


@router.subscriber(
    settings.broker.image_color_to_grayscale_topic,
    group_id=settings.broker.image_color_to_grayscale_group,
    no_ack=True,
    description="Kafka message handler for colorization image"
)
async def handle_image_color_to_grayscale_topic(
        schemas: ConvertColorImageSchema,
        msg: KafkaMessage,
        logger: Logger,
        bootstrap: FromDishka[Bootstrap]
) -> None:
    logger.info("handling colorization image event from telegram")

    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        ConvertColorToGrayScaleAndSendToChatEvent(
            data=schemas.image.data,
            width=schemas.image.width,
            height=schemas.image.height,
            chat_id=schemas.chat_id,
            name=schemas.image.name,
        )
    )

    await msg.ack()

    logger.info("successfully handled colorization image event from telegram")


@router.subscriber(
    settings.broker.image_inverse_topic,
    group_id=settings.broker.image_inverse_group,
    no_ack=True,
    description="Kafka message handler for inverse image"
)
async def handle_image_inverse_topic(
        schemas: ConvertColorImageSchema,
        msg: KafkaMessage,
        logger: Logger,
        bootstrap: FromDishka[Bootstrap],
) -> None:
    logger.info("handling inverse image event from telegram")
    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        ConvertImageInversionAndSendToChatEvent(
            data=schemas.image.data,
            width=schemas.image.width,
            height=schemas.image.height,
            chat_id=schemas.chat_id,
            name=schemas.image.name,
        )
    )

    await msg.ack()

    logger.info("successfully handled inverse image event from telegram")
