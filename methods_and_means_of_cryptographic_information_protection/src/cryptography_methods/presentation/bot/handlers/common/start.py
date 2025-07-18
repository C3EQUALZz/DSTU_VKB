from typing import Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from dishka import FromDishka

from cryptography_methods.application.commands.user.register_via_telegram import (
    RegisterUserViaTelegramCommandHandler,
    RegisterUserViaTelegramCommand
)

router: Final[Router] = Router()


@router.message(CommandStart())
async def cmd_start_handler(message: Message, interactor: FromDishka[RegisterUserViaTelegramCommandHandler]) -> None:
    command: RegisterUserViaTelegramCommand = RegisterUserViaTelegramCommand(
        first_name=message.from_user.first_name,
        telegram_id=message.from_user.id,
        is_bot=message.from_user.is_bot,
        second_name=message.from_user.last_name,
        middle_name=None,
    )

    await interactor(data=command)

    await message.reply(
        text="Приветствую, вас! Я бот, который создан для лабораторных работ по криптографии"
    )
