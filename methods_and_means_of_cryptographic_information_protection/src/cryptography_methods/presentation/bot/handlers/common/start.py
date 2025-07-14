from typing import Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from dishka import FromDishka

from cryptography_methods.application.commands.user.greetings import (
    GreetingUserCommandHandler,
    GreetingUserCommand
)

router: Final[Router] = Router()


@router.message(CommandStart())
async def cmd_start_handler(message: Message, interactor: FromDishka[GreetingUserCommandHandler]) -> None:
    command: GreetingUserCommand = GreetingUserCommand(
        first_name=message.from_user.first_name
    )

    await interactor(data=command)
