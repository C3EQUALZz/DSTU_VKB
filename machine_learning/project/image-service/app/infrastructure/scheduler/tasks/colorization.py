import logging
from logging import Logger
from typing import Final

from dishka import FromDishka
from dishka.integrations.taskiq import inject

from app.infrastructure.scheduler import scheduler
from app.domain.entities.image import ImageEntity
from app.domain.values.image import PositiveNumber, ImageName
from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.factory import TaskTopicFactory
from app.infrastructure.scheduler.tasks.schemas import PhotoForSendToChatSchema, \
    PairOfPhotosForStylizationAndForSendToChatSchema
from app.infrastructure.services.colorization import ImageColorizationService
from app.settings.configs.enums import TaskNamesConfig

logger: Final[Logger] = logging.getLogger(__name__)


@scheduler.task(task_name=TaskNamesConfig.RGB_TO_GRAYSCALE)
@inject(patch_module=True)
async def convert_rgb_to_grayscale_task(
        schemas: PhotoForSendToChatSchema,
        service: FromDishka[ImageColorizationService],
        topic_factory: FromDishka[TaskTopicFactory],
        broker: FromDishka[BaseMessageBroker]
) -> None:
    logger.debug(f"Started completing task convert_rgb_to_grayscale_task....")

    image_entity: ImageEntity = ImageEntity(
        data=schemas.data,
        width=PositiveNumber(schemas.width),
        height=PositiveNumber(schemas.height),
        name=ImageName(schemas.name),
    )

    colorized_photo: ImageEntity = service.convert_rgb_to_grayscale(image_entity)

    topic_name: str = topic_factory.get_topic(TaskNamesConfig.RGB_TO_GRAYSCALE)

    await broker.send_message(topic=topic_name, value=schemas.from_(colorized_photo, schemas.chat_id))


@scheduler.task(task_name=TaskNamesConfig.GRAYSCALE_TO_RGB)
@inject(patch_module=True)
async def convert_grayscale_to_rgb_task(
        schemas: PhotoForSendToChatSchema,
        service: FromDishka[ImageColorizationService],
        topic_factory: FromDishka[TaskTopicFactory],
        broker: FromDishka[BaseMessageBroker]
) -> None:
    logger.debug(f"Started completing task convert_grayscale_to_rgb_task....")

    image_entity: ImageEntity = ImageEntity(
        data=schemas.data,
        width=PositiveNumber(schemas.width),
        height=PositiveNumber(schemas.height),
        name=ImageName(schemas.name),
    )

    gray_photo: ImageEntity = service.convert_grayscale_to_rgb(image_entity)

    topic_name: str = topic_factory.get_topic(TaskNamesConfig.GRAYSCALE_TO_RGB)

    await broker.send_message(topic=topic_name, value=schemas.from_(gray_photo, schemas.chat_id))


@scheduler.task(task_name=TaskNamesConfig.STYLIZATION)
@inject(patch_module=True)
async def convert_stylization_task(
        schemas: PairOfPhotosForStylizationAndForSendToChatSchema,
        service: FromDishka[ImageColorizationService],
        topic_factory: FromDishka[TaskTopicFactory],
        broker: FromDishka[BaseMessageBroker]
) -> None:
    logger.debug(f"Started completing task convert_stylization_task....")

    original_image_entity: ImageEntity = ImageEntity(
        data=schemas.original.data,
        width=PositiveNumber(schemas.original.width),
        height=PositiveNumber(schemas.original.height),
        name=ImageName(schemas.original.name),
    )

    style_image_entity: ImageEntity = ImageEntity(
        data=schemas.style.data,
        width=PositiveNumber(schemas.style.width),
        height=PositiveNumber(schemas.style.height),
        name=ImageName(schemas.style.name),
    )

    styled_image: ImageEntity = service.style_image(
        original_image=original_image_entity,
        styling_template=style_image_entity
    )

    topic_name: str = topic_factory.get_topic(TaskNamesConfig.STYLIZATION)

    await broker.send_message(
        topic=topic_name,
        value=PhotoForSendToChatSchema.from_(
            styled_image,
            schemas.original.chat_id,
        )
    )
