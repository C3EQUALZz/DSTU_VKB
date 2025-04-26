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
from app.infrastructure.scheduler.tasks.schemas import PhotoNewWidthNewHeightForSendToChatSchema, \
    PhotoForSendToChatSchema
from app.infrastructure.services.transform import ImageTransformService
from app.settings.configs.enums import TaskNamesConfig

logger: Final[Logger] = logging.getLogger(__name__)


@scheduler.task(task_name=TaskNamesConfig.CROP)
@inject(patch_module=True)
async def convert_crop_task(
        schemas: PhotoNewWidthNewHeightForSendToChatSchema,
        service: FromDishka[ImageTransformService],
        topic_factory: FromDishka[TaskTopicFactory],
        broker: FromDishka[BaseMessageBroker]
) -> None:
    logger.debug("Started completing task convert_crop_task")

    image_entity: ImageEntity = ImageEntity(
        data=schemas.data,
        width=PositiveNumber(schemas.old_width),
        height=PositiveNumber(schemas.old_height),
        name=ImageName(schemas.name),
    )

    cropped_photo: ImageEntity = service.crop(image_entity, new_width=schemas.new_width, new_height=schemas.new_height)

    topic_name: str = topic_factory.get_topic(TaskNamesConfig.CROP)

    await broker.send_message(
        topic_name,
        value=schemas.from_(
            cropped_photo,
            chat_id=schemas.chat_id,
            new_width=schemas.new_width,
            new_height=schemas.new_height,
        )
    )


@scheduler.task(task_name=TaskNamesConfig.ROTATION)
@inject(patch_module=True)
async def convert_rotation_task(
        schemas: PhotoForSendToChatSchema,
        service: FromDishka[ImageTransformService],
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

    rotated_photo: ImageEntity = service.rotate(image_entity)

    topic_name: str = topic_factory.get_topic(TaskNamesConfig.ROTATION)

    await broker.send_message(
        topic=topic_name,
        value=schemas.from_(
            entity=rotated_photo,
            chat_id=schemas.chat_id
        )
    )
