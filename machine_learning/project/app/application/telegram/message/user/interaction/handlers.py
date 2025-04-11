from aiogram import Router
from aiogram.filters import (
    Command,
    CommandStart,
)
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f"Привет, твой ID: {message.from_user.id}")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Это команда help")
