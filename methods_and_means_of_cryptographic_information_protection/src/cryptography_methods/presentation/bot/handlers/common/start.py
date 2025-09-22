from typing import Final

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message

from cryptography_methods.presentation.bot.filters.chat import ChatTypeFilter

router: Final[Router] = Router()


@router.message(
    ChatTypeFilter(allowed_chat_types=[ChatType.PRIVATE]),
    CommandStart()
)
async def cmd_start_handler(
        message: Message,
) -> None:
    await message.reply(
        text=f"Приветствую, вас { message.from_user.username } 👋! Я бот, который создан для лабораторных работ по криптографии"
    )
