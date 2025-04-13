from aiogram import Bot
from aiogram.types.input_file import BufferedInputFile
from taskiq import TaskiqDepends

from app.application.jobs import broker
from app.domain.entities.message import ImageMessageEntity
from app.infrastructure.services.image import ImageService


@broker.task(task_name="my_task")
async def colorize_photo(service: ImageService, image: ImageMessageEntity, bot: Bot = TaskiqDepends()) -> None:
    colorized_photo: ImageMessageEntity = await service.colorize_image(image)
    await bot.send_photo(
        chat_id=image.chat_id,
        photo=BufferedInputFile(colorized_photo.photo, filename="converted.jpg")
    )
