from typing import Final

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext

from app.application.telegram.fsms.app import AppState

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


@router.message(AppState.PROCESSING)
async def stop_flood(message: Message, i18n: I18nContext) -> None:
    """
    A stub in case the user has previously written
    """
    await message.answer(i18n.get("stop-flood"))
