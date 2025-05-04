import logging
from logging import Logger
from typing import Final

from aiogram import Bot
from aiogram.types import BufferedInputFile
from dishka.integrations.taskiq import inject
from taskiq import TaskiqDepends

from app.infrastructure.scheduler import scheduler
from app.infrastructure.scheduler.tasks.images.schemas import ImageForSendToChatSchema
from app.settings.configs.enums import TaskNamesConfig


logger: Final[Logger] = logging.getLogger(__name__)


@scheduler.task(task_name=TaskNamesConfig.SEND_CONVERTED_IMAGE_TO_USER.value)
@inject(patch_module=True)
async def send_converted_image_task(
        schemas: ImageForSendToChatSchema,
        bot: Bot = TaskiqDepends()
) -> None:
    logger.info("Sending converted image to user with id=%s", schemas.chat_id)

    await bot.send_photo(
        chat_id=schemas.chat_id,
        photo=BufferedInputFile(
            schemas.data,
            filename=schemas.name
        )
    )

@scheduler.task(task_name=TaskNamesConfig.IMAGE_METADATA.value)
@inject(patch_module=True)
async def send_metadata_from_image_task(
        bot: Bot = TaskiqDepends()
) -> None:
    ...