from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.application.telegram.message.user.text.state_machines import AIBotResponseStateMachine

router = Router(name="chatbot-router")


@router.message()
async def cmd_generate_text_message_for_chatbot(
        message: Message,
        state: FSMContext,
):
    await state.set_state(AIBotResponseStateMachine.wait)
