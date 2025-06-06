import logging
from logging import Logger
from typing import Final

from aiogram import Bot
from aiogram.enums import ParseMode
from chatgpt_md_converter import telegram_format
from dishka.integrations.taskiq import inject
from taskiq import TaskiqDepends

from app.infrastructure.scheduler import scheduler
from app.infrastructure.scheduler.tasks.texts.schemas import TextForSendToChatSchema
from app.settings.configs.enums import TaskNamesConfig

logger: Final[Logger] = logging.getLogger(__name__)


@scheduler.task(
    task_name=TaskNamesConfig.SEND_TEXT_TO_USER.value,
    retry_on_error=True
)
@inject(patch_module=True)
async def send_text_from_llm_to_user_task(
        schemas: TextForSendToChatSchema,
        bot: Bot = TaskiqDepends()
) -> None:
    logger.info("Sending text to user with id=%s", schemas.chat_id)

    await bot.send_message(
        chat_id=schemas.chat_id,
        text=telegram_format(schemas.content),
        parse_mode=ParseMode.HTML
    )
