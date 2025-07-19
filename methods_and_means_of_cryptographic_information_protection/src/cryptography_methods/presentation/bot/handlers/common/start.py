from typing import Final

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext
from dishka import FromDishka

from cryptography_methods.application.commands.user.register_via_telegram import (
    RegisterUserViaTelegramCommandHandler,
    RegisterUserViaTelegramCommand
)
from cryptography_methods.presentation.bot.filters.chat import ChatTypeFilter
from cryptography_methods.presentation.bot.handlers.common.consts import HELLO

router: Final[Router] = Router()


@router.message(
    ChatTypeFilter(allowed_chat_types=[ChatType.PRIVATE]),
    CommandStart()
)
async def cmd_start_handler(
        message: Message,
        interactor: FromDishka[RegisterUserViaTelegramCommandHandler],
        i18n: I18nContext
) -> None:
    command: RegisterUserViaTelegramCommand = RegisterUserViaTelegramCommand(
        first_name=message.from_user.first_name,
        telegram_id=message.from_user.id,
        is_bot=message.from_user.is_bot,
        second_name=message.from_user.last_name,
        middle_name=None,
    )

    await interactor(data=command)

    await message.reply(
        text=i18n.get(HELLO, user=message.from_user.first_name)
    )
