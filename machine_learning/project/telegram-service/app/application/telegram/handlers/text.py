from typing import (
    Final,
    TYPE_CHECKING,
)

from aiogram import (
    F,
    Router,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dishka import FromDishka

from app.application.telegram.fsms.app import AppState
from app.logic.bootstrap import Bootstrap
from app.logic.commands.texts import SendTextMessageToChatBotCommand

if TYPE_CHECKING:
    from app.logic.message_bus import MessageBus

router: Final[Router] = Router(name=__name__)


@router.message(AppState.TEXT.ACTIVATE, F.text & ~F.text.startswith("/") & ~F.text.startswith("@"))
async def cmd_generate_text_message_for_chatbot(
        message: Message, state: FSMContext, bootstrap: FromDishka[Bootstrap]
) -> None:
    """
    This handler generates text message from chatbot. It is used for providing info about chatgpt.
    :param message: Telegram message from user.
    :param state: Current state of FSM, using to avoiding flood.
    :param bootstrap: Bootstrap class taken from IoC.
    """
    await state.set_state(AppState.PROCESSING)

    message_bus: MessageBus = await bootstrap.get_messagebus()
    await message_bus.handle(SendTextMessageToChatBotCommand(content=message.text, chat_id=message.chat.id))

    await state.set_state(AppState.TEXT.ACTIVATE)
