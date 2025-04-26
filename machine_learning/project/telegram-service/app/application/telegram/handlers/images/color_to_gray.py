from typing import Final

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka import FromDishka

from app.application.telegram.fsms.app import AppState
from app.application.telegram.keyboards.callbacks.images import ImageClickActionCallback
from app.application.telegram.keyboards.images import ImageCLickAction
from app.application.telegram.middlewares.processing import ProcessingMiddleware
from app.domain.entities.message import ImageEntity
from app.logic.bootstrap import Bootstrap
from app.logic.commands.images import ConvertColorImageToGrayScaleImageCommand
from app.logic.message_bus import MessageBus

router: Final[Router] = Router(name=__name__)
router.message.middleware(ProcessingMiddleware())


@router.callback_query(
    AppState.IMAGE.ACTION_SELECTION,
    ImageClickActionCallback.filter(F.action == ImageCLickAction.COLOR_TO_GRAY)  # type: ignore
)
async def handle_color_to_gray(
        query: CallbackQuery,
        state: FSMContext,
        bootstrap: FromDishka[Bootstrap]
) -> None:
    image_entity: ImageEntity = (await state.get_data())["context"]
    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        ConvertColorImageToGrayScaleImageCommand(
            data=image_entity.data,
            name=image_entity.name,
            height=image_entity.height,
            width=image_entity.width,
            chat_id=query.message.chat_id,
        )
    )

    await state.set_state(AppState.IMAGE.WAITING_PHOTO)
