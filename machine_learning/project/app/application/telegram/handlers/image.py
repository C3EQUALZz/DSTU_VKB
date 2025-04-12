from typing import Final

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from app.application.telegram.fsms.image import ImageStateMachine
from app.application.telegram.keyboards.callbacks.images import ImageClickActionCallback
from app.application.telegram.keyboards.images import build_keyboard

router: Final[Router] = Router(name=__name__)


@router.message(Command("image"))
async def start_painter_mode(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    """

    :param message:
    :param state:
    :param i18n:
    :return:
    """
    await state.set_state(ImageStateMachine.wait_for_message)
    await message.answer(text=i18n.get("image-bot-mode"), reply_markup=build_keyboard().as_markup())


@router.callback_query(ImageClickActionCallback.filter())
async def handle_callback(query: CallbackQuery, callback_data: ImageClickActionCallback) -> None:
    await query.answer()
    await query.message.answer(f"Вы выбрали: <b>{callback_data.name}</b>")
