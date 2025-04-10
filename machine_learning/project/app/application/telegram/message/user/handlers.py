from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.reply(f"Привет, твой ID: {message.from_user.id}")


@router.message(Command("help"))
async def get_help(message: Message):
    await message.answer("Это команда help")

