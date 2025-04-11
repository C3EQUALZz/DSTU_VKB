from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.filters import (
    CommandStart,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.application.telegram.message.user.text.fsm import TextStateMachine

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.reply("Привет!")


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer("Это команда help")


@router.message(Command("cancel"), F.state.as_("current_state"))
async def universal_cancel(
        message: Message,
        state: FSMContext,
        current_state: str
):
    mode_names = {
        TextStateMachine: "текстового режима",
        # AudioMode: "аудио режима",
        # ImageMode: "режима обработки изображений"
    }

    for mode_class, mode_name in mode_names.items():
        if current_state in mode_class.states:
            await state.clear()
            await message.answer(f"❌ Выход из {mode_name}")
            return

    await message.answer("⚠️ Нет активных режимов для отмены")
