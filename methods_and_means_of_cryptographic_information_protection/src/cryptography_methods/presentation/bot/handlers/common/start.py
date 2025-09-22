from typing import Final

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext

from cryptography_methods.presentation.bot.filters.chat import ChatTypeFilter
from cryptography_methods.presentation.bot.handlers.common.consts import HELLO

router: Final[Router] = Router()


@router.message(
    ChatTypeFilter(allowed_chat_types=[ChatType.PRIVATE]),
    CommandStart()
)
async def cmd_start_handler(
        message: Message,
        i18n: I18nContext
) -> None:
    await message.reply(
        text=f"Приветствую, вас { message.from_user.username } 👋! Я бот, который создан для лабораторных работ по криптографии"
    )
