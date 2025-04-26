from typing import Final

from aiogram import (
    F,
    Router,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)
from dishka import FromDishka

from app.application.telegram.fsms.app import AppState
from app.application.telegram.keyboards.callbacks.images import ImageClickActionCallback
from app.application.telegram.keyboards.images import ImageCLickAction
from app.application.telegram.middlewares.processing import ProcessingMiddleware
from app.domain.entities.message import ImageEntity
from app.logic.bootstrap import Bootstrap
from app.logic.commands.images import CropImageCommand
from app.logic.message_bus import MessageBus


router: Final[Router] = Router(name=__name__)
router.message.middleware(ProcessingMiddleware())


@router.callback_query(
    AppState.IMAGE.ACTION_SELECTION,
    ImageClickActionCallback.filter(F.action == ImageCLickAction.CROP)  # type: ignore
)
async def handle_crop_and_send_message_action(
        query: CallbackQuery,
        callback_data: ImageClickActionCallback,
        state: FSMContext
) -> None:
    await state.set_state(AppState.IMAGE.CROP_PARAMS)
    await query.message.answer("Введите новую ширину и высоту через пробел")
    await query.answer()


@router.message(
    AppState.IMAGE.CROP_PARAMS,
    F.text.regexp(r"^\d+ \d+$")
)
async def handle_crop_action(
        message: Message,
        state: FSMContext,
        bootstrap: FromDishka[Bootstrap],
) -> None:
    width, height = map(int, message.text.split())
    message_bus: MessageBus = await bootstrap.get_messagebus()
    image_entity: ImageEntity = (await state.get_data())["context"]

    await message_bus.handle(
        CropImageCommand(
            data=image_entity.data,
            chat_id=message.chat.id,
            name=image_entity.name,
            old_width=image_entity.width,
            old_height=image_entity.height,
            new_width=width,
            new_height=height,
        )
    )

    await state.set_state(AppState.IMAGE.WAITING_PHOTO)
