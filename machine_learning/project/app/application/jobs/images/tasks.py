import logging

from aiogram import Bot
from aiogram.types import BufferedInputFile
from dishka import FromDishka
from dishka.integrations.taskiq import inject
from taskiq import TaskiqDepends

from app.application.jobs import broker
from app.application.jobs.images.schemas import ColorizePhotoSchema
from app.domain.entities.message import ImageMessageEntity
from app.infrastructure.services.image import ImageService

logger = logging.getLogger(__name__)


@broker.task(task_name="my_task")
@inject(patch_module=True)
async def colorize_photo(
        schemas: ColorizePhotoSchema,
        service: FromDishka[ImageService],
        bot: Bot = TaskiqDepends()
) -> None:
    image_entity: ImageMessageEntity = ImageMessageEntity(
        photo=schemas.photo,
        chat_id=schemas.chat_id,
    )

    colorized_photo: ImageMessageEntity = await service.colorize_image(image_entity)

    await bot.send_photo(
        chat_id=colorized_photo.chat_id,
        photo=BufferedInputFile(colorized_photo.photo, filename="converted.jpg")
    )
