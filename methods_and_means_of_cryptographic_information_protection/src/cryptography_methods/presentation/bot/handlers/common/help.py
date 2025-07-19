from typing import Final

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext

from cryptography_methods.presentation.bot.filters.chat import ChatTypeFilter
from cryptography_methods.presentation.bot.handlers.common.consts import HELP

router: Final[Router] = Router()


@router.message(
    ChatTypeFilter(allowed_chat_types=[ChatType.PRIVATE]),
    Command(commands=[HELP])
)
async def cmd_help_handler(message: Message, i18n: I18nContext) -> None:
    await message.reply(i18n.get(HELP))
