from typing import Final

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from app.application.telegram.fsms.app import AppState
from app.application.telegram.keyboards.callbacks.images import ImageClickActionCallback, ImageCLickAction
from app.application.telegram.keyboards.images import build_keyboard
from dishka.integrations.aiogram import FromDishka

from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.message_bus import MessageBus

router: Final[Router] = Router(name=__name__)


@router.message(Command("image"))
async def start_painter_mode(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    """
    :param message:
    :param state:
    :param i18n:
    :return:
    """
    await state.set_state(AppState.IMAGE.ACTIVATE)
    await message.answer(text=i18n.get("image-bot-mode"), reply_markup=build_keyboard(i18n).as_markup())


@router.callback_query(
    AppState.IMAGE.ACTIVATE,
    ImageClickActionCallback.filter()
)
async def say_to_user(
        query: CallbackQuery,
        callback_data: ImageClickActionCallback,
        state: FSMContext,
        i18n: I18nContext
) -> None:
    await state.update_data(selected_action=callback_data.action)
    await state.set_state(AppState.IMAGE.WAITING)
    await query.message.answer("📷 Пришли изображение для обработки")
    await query.answer()


@router.message(
    AppState.IMAGE.WAITING,
    F.photo,
)
async def handle_gray_to_color(
        message: Message,
        state: FSMContext,
        bootstrap: FromDishka[Bootstrap[UsersUnitOfWork]]
) -> None:
    data = await state.get_data()
    action_raw = data.get("selected_action")
    message_bus: MessageBus = await bootstrap.get_messagebus()

    try:
        action = ImageCLickAction(action_raw)
    except ValueError:
        await message.answer("❌ Неизвестное действие")
        return

    message_bus.handle(

    )

    await state.set_state(AppState.PROCESSING)
    await message.answer("Фото получено. Обрабатываем...")
    await state.set_state(AppState.IMAGE.ACTIVATE)
