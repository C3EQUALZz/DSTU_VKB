from typing import Final

from aiogram import Router
from aiogram.filters import (
    Command,
    CommandStart,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

from app.application.telegram.fsms.app import AppState, StartStateGroup

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def cmd_start(
        message: Message,
        i18n: I18nContext,
        state: FSMContext,
) -> None:
    """
    Command for start bot, here you must provide
    :param message: start message `/start`
    :param i18n: object that is using for translation messages.
    :param state: start state `/start`
    :return: nothing
    """
    await message.reply(i18n.get("hello", user=message.from_user.username))
    await state.set_state(StartStateGroup.WAITING)


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
