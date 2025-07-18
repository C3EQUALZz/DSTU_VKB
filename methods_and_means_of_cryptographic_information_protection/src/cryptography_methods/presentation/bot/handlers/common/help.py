from aiogram import Router, F
from typing import Final

from aiogram.filters import Command
from aiogram.types import Message

from cryptography_methods.presentation.bot.handlers.common.consts import HELP

router: Final[Router] = Router()


@router.message(Command(commands=[HELP]))
async def cmd_help_handler(message: Message) -> None:
    ...
