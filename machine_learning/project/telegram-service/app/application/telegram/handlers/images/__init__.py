import logging
from logging import Logger
from typing import Final

from aiogram import (
    F,
    Router,
)
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    File,
    Message,
    PhotoSize,
)
from aiogram_i18n import I18nContext

from app.application.telegram.fsms.app import AppState
from app.application.telegram.handlers.images.color_to_gray import router as router_color_to_gray
from app.application.telegram.handlers.images.crop import router as router_crop
from app.application.telegram.handlers.images.gray_to_color import router as router_gray_to_color
from app.application.telegram.handlers.images.metadata import router as router_metadata
from app.application.telegram.handlers.images.rotate import router as router_rotate
from app.application.telegram.keyboards.callbacks.images import ImageClickActionCallback
from app.application.telegram.keyboards.images import build_keyboard
from app.domain.entities.message import ImageEntity


router: Final[Router] = Router(name=__name__)

router.include_router(router_metadata)
router.include_router(router_crop)
router.include_router(router_gray_to_color)
router.include_router(router_color_to_gray)
router.include_router(router_rotate)

logger: Final[Logger] = logging.getLogger(__name__)


# @router.callback_query(
#     AppState.IMAGE.ACTION_SELECTION,
#     ImageClickActionCallback.filter()
# )
# async def change_message(
#         query: CallbackQuery,
#         callback_data: ImageClickActionCallback,
#         state: FSMContext,
#         i18n: I18nContext
# ) -> None:
#     # Автоматически редактируем сообщение сразу при нажатии
#     try:
#
#         await query.message.edit_text(
#             text="Обрабатываю изображение",
#             reply_markup=None
#         )
#
#     except TelegramBadRequest:
#         pass  # Ес


@router.message(
    AppState.IMAGE.WAITING_PHOTO,
    F.photo,
)
async def handle_image_waiting(
        message: Message,
        state: FSMContext,
        i18n: I18nContext,
) -> None:
    photo: PhotoSize = message.photo[-1]
    file: File = await message.bot.get_file(photo.file_id)
    image_data: bytes = (await message.bot.download_file(file.file_path)).read()

    image_entity: ImageEntity = ImageEntity(
        data=image_data,
        name=file.file_path,
        height=photo.height,
        width=photo.width,
    )

    message_with_choice: Message = await message.answer(
        i18n.get("choose-action"),
        reply_markup=build_keyboard(i18n).as_markup()
    )

    await state.update_data(message_with_choice_id=message_with_choice.message_id)
    await state.update_data(context=image_entity)

    await state.set_state(AppState.IMAGE.ACTION_SELECTION)
