from typing import TYPE_CHECKING

from aiogram import (
    F,
    Router,
)

from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from chatgpt_md_converter import telegram_format
from dishka import FromDishka

from app.application.telegram.message.user.text.fsm import TextStateMachine
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.messages import SendTextMessageToChatBot

if TYPE_CHECKING:
    from app.domain.entities.message import TextMessageEntity
    from app.logic.message_bus import MessageBus

router = Router(name="chatbot-router")


@router.message(Command("text"))
async def start_chat_mode(message: Message, state: FSMContext) -> None:
    await state.set_state(TextStateMachine.wait_for_message)
    await message.answer(
        "📝 Режим чат-бота активирован!\n"
        "Теперь все ваши сообщения будут обрабатываться ИИ\n"
        "Для выхода используйте /cancel"
    )


@router.message(TextStateMachine.processing)
async def stop_flood(message: Message) -> None:
    """
    A stub in case the user has previously written
    """
    await message.answer("⏳ Ваш предыдущий запрос еще обрабатывается...")


@router.message(
    TextStateMachine.wait_for_message,
    F.text & ~F.text.startswith("/") & ~F.text.startswith("@")
)
async def cmd_generate_text_message_for_chatbot(
        message: Message, state: FSMContext, bootstrap: FromDishka[Bootstrap[UsersUnitOfWork]]
) -> None:
    """
    This handler generates text message from chatbot. It is used for providing info about chatgpt.
    :param message: Telegram message from user.
    :param state: Current state of FSM, using to avoiding flood.
    :param bootstrap: Bootstrap class taken from IoC.
    """
    await state.set_state(TextStateMachine.processing)

    message_bus: MessageBus = await bootstrap.get_messagebus()
    await message_bus.handle(SendTextMessageToChatBot(content=message.text))
    reply_from_bot: TextMessageEntity = message_bus.command_result

    await message.answer(
        telegram_format(reply_from_bot.content.as_generic_type()),
        parse_mode=ParseMode.HTML
    )

    await state.set_state(TextStateMachine.wait_for_message)
