from typing import Final

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

from app.application.telegram.fsms.text import TextStateMachine

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, i18n: I18nContext) -> None:
    """
    Command for start bot, here you must provide
    :param message:
    :param i18n:
    :return:
    """
    await message.reply(i18n.get("hello", user=message.from_user.username))


@router.message(Command("help"))
async def cmd_help(message: Message, i18n: I18nContext) -> None:
    await message.answer(i18n.get("help"))


@router.message(Command("settings"))
async def cmd_settings(message: Message, i18n: I18nContext) -> None:
    ...


@router.message(Command("text"))
async def cmd_start_chat_mode(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    await state.set_state(TextStateMachine.wait_for_message)
    await message.answer(i18n.get("chat-bot-mode"))


@router.message(Command("cancel"), F.state.as_("current_state"))
async def cmd_universal_cancel(
        message: Message,
        state: FSMContext,
        current_state: str
) -> None:
    mode_names = {
        TextStateMachine: "текстового режима",
        # AudioMode: "аудио режима",
        # ImageMode: "режима обработки изображений"
    }

    for mode_class, mode_name in mode_names.items():
        if current_state in mode_class.__states__:
            await state.clear()
            await message.answer(f"❌ Выход из {mode_name}")
            return

    await message.answer("⚠️ Нет активных режимов для отмены")
