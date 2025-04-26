import logging
from typing import Final

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka import FromDishka

from app.application.telegram.fsms.app import AppState
from app.application.telegram.keyboards.callbacks.images import ImageClickActionCallback
from app.application.telegram.keyboards.images import ImageCLickAction
from app.application.telegram.middlewares.processing import ProcessingMiddleware
from app.domain.entities.message import ImageEntity
from app.logic.bootstrap import Bootstrap
from app.logic.commands.images import GetMetadataFromImageCommand
from app.logic.message_bus import MessageBus

router: Final[Router] = Router(name=__name__)
router.message.middleware(ProcessingMiddleware())

logger: Final[logging.Logger] = logging.getLogger(__name__)


@router.callback_query(
    AppState.IMAGE.ACTION_SELECTION,
    ImageClickActionCallback.filter(F.action == ImageCLickAction.METADATA)  # type: ignore
)
async def handle_metadata(
        query: CallbackQuery,
        state: FSMContext,
        bootstrap: FromDishka[Bootstrap]
) -> None:
    image_entity: ImageEntity = (await state.get_data())["context"]
    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        GetMetadataFromImageCommand(
            data=image_entity.data,
            name=image_entity.name,
            chat_id=query.message.chat_id,
            width=image_entity.width,
            height=image_entity.height,
        )
    )

    await state.set_state(AppState.IMAGE.WAITING_PHOTO)
