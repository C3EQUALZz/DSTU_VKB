from typing import TYPE_CHECKING, Final

from aiogram import (
    F,
    Router,
)
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext
from chatgpt_md_converter import telegram_format
from dishka import FromDishka

from app.application.telegram.fsms.app import AppState
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.texts import SendTextMessageToChatBotCommand

if TYPE_CHECKING:
    from app.domain.entities.message import TextMessageEntity
    from app.logic.message_bus import MessageBus

router: Final[Router] = Router(name=__name__)


@router.message(Command("text"))
async def cmd_start_chat_mode(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    await state.set_state(AppState.TEXT.ACTIVATE)
    await message.answer(i18n.get("chat-bot-mode"))


@router.message(AppState.TEXT.ACTIVATE, F.text & ~F.text.startswith("/") & ~F.text.startswith("@"))
async def cmd_generate_text_message_for_chatbot(
    message: Message, state: FSMContext, bootstrap: FromDishka[Bootstrap[UsersUnitOfWork]]
) -> None:
    """
    This handler generates text message from chatbot. It is used for providing info about chatgpt.
    :param message: Telegram message from user.
    :param state: Current state of FSM, using to avoiding flood.
    :param bootstrap: Bootstrap class taken from IoC.
    """
    await state.set_state(AppState.PROCESSING)

    message_bus: MessageBus = await bootstrap.get_messagebus()
    await message_bus.handle(SendTextMessageToChatBotCommand(content=message.text))
    reply_from_bot: TextMessageEntity = message_bus.command_result

    await message.answer(telegram_format(reply_from_bot.content.as_generic_type()), parse_mode=ParseMode.HTML)

    await state.set_state(AppState.TEXT.ACTIVATE)
