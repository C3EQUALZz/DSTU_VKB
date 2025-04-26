from typing import (
    Any,
    Final,
)

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext
from aiogram import F
from dishka import FromDishka

from app.application.telegram.fsms.app import AppState
from app.application.telegram.keyboards.callbacks.images import ImageClickActionCallback
from app.application.telegram.keyboards.images import ImageCLickAction
from app.application.telegram.middlewares.processing import ProcessingMiddleware
from app.domain.entities.message import ImageEntity
from app.logic.bootstrap import Bootstrap
from app.logic.commands.images import ConvertGrayScaleImageToColorImageCommand
from app.logic.message_bus import MessageBus

router: Final[Router] = Router(name=__name__)
router.message.middleware(ProcessingMiddleware())


@router.callback_query(
    AppState.IMAGE.ACTION_SELECTION,
    ImageClickActionCallback.filter(F.action == ImageCLickAction.GRAY_TO_COLOR)  # type: ignore
)
async def handle_gray_to_color(
        query: CallbackQuery,
        state: FSMContext,
        bootstrap: FromDishka[Bootstrap],
        i18n: I18nContext,
) -> None:
    data_from_state: dict[str, Any] = await state.get_data()
    image_entity: ImageEntity = data_from_state["context"]
    message_bus: MessageBus = await bootstrap.get_messagebus()

    await state.set_state(AppState.PROCESSING)

    await message_bus.handle(
        ConvertGrayScaleImageToColorImageCommand(
            data=image_entity.data,
            name=image_entity.name,
            height=image_entity.height,
            width=image_entity.width,
            chat_id=query.message.chat.id,
        )
    )

    await state.set_state(AppState.IMAGE.WAITING_PHOTO)
