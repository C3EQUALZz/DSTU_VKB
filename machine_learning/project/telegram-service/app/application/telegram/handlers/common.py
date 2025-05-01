from typing import Final

from aiogram import Router
from aiogram.filters import (
    Command,
    CommandStart,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.application.telegram.fsms.app import AppState
from app.logic.commands.users import CreateUserCommand
from app.logic.message_bus import MessageBus

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def cmd_start(
        message: Message,
        i18n: I18nContext,
        message_bus: FromDishka[MessageBus]) -> None:
    """
    Command for start bot, here you must provide
    :param message: start message `/start`
    :param i18n: object that is using for translation messages
    :param message_bus: Message Bus taken from IoC
    :return: nothing
    """
    await message.reply(i18n.get("hello", user=message.from_user.username))

    username: str = message.from_user.username if message.from_user.username else message.from_user.first_name
    language_code: str = message.from_user.language_code if message.from_user.language_code else "ru"
    role: str = message.from_user.is_bot if message.from_user.is_bot else "user"

    await message_bus.handle(
        CreateUserCommand(
            user_id=message.from_user.id,
            full_name=message.from_user.full_name,
            user_login=username,
            language_code=language_code,
            role=role
        )
    )


@router.message(Command("help"))
async def cmd_help(message: Message, i18n: I18nContext) -> None:
    """
    Command for getting help commands of bot
    """
    await message.answer(i18n.get("help"))


@router.message(Command("settings"))
async def cmd_settings(message: Message, i18n: I18nContext) -> None: ...


@router.message(Command("image"))
async def cmd_image_mode(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    """
    :param message: Message from user which would be used
    :param state:
    :param i18n:
    :return:
    """
    await state.set_state(AppState.IMAGE.WAITING_PHOTO)
    await message.answer(i18n.get("image-bot-mode"))
    await message.answer(i18n.get("send-image-for-processing"))


@router.message(Command("text"))
async def cmd_start_chat_mode(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    await state.set_state(AppState.TEXT.ACTIVATE)
    await message.answer(i18n.get("chat-bot-mode"))
