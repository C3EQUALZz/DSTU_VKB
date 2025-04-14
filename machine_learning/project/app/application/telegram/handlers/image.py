from typing import TYPE_CHECKING, Any, Final

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, File, Message, PhotoSize
from aiogram_i18n import I18nContext
from dishka.integrations.aiogram import FromDishka

from app.application.telegram.fsms.app import AppState
from app.application.telegram.keyboards.callbacks.images import ImageCLickAction, ImageClickActionCallback
from app.application.telegram.keyboards.images import build_keyboard
from app.infrastructure.factories.image import ImageCommandFactory
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap

if TYPE_CHECKING:
    from app.logic.message_bus import MessageBus

router: Final[Router] = Router(name=__name__)


@router.message(Command("image"))
async def cmd_image_mode(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    """
    :param message: Message from user which would be used
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
async def keyboard_callback(
        query: CallbackQuery,
        callback_data: ImageClickActionCallback,
        state: FSMContext,
        i18n: I18nContext
) -> None:
    await state.update_data(selected_action=callback_data.action)
    await state.set_state(AppState.IMAGE.WAITING)
    await query.message.answer(i18n.get("send-image-for-processing"))
    await query.answer()


@router.message(
    AppState.IMAGE.WAITING,
    F.photo,
)
async def handle_image_processing_with_ai(
        message: Message,
        state: FSMContext,
        bootstrap: FromDishka[Bootstrap[UsersUnitOfWork]],
        factory: FromDishka[ImageCommandFactory],
        i18n: I18nContext
) -> None:
    fsm_state_data: dict[str, Any] = await state.get_data()
    action_raw: str = fsm_state_data.get("selected_action")

    message_bus: MessageBus = await bootstrap.get_messagebus()
    photo: PhotoSize = message.photo[-1]
    file: File = await message.bot.get_file(photo.file_id)
    image_data: bytes = (await message.bot.download_file(file.file_path)).read()

    action: ImageCLickAction = ImageCLickAction(action_raw)

    await state.set_state(AppState.PROCESSING)
    await message.answer(i18n.get("image-processing"))

    await message_bus.handle(
        factory.create(
            action.value,
            chat_id=message.chat.id,
            data=image_data
        )
    )

    await state.set_state(AppState.IMAGE.ACTIVATE)
