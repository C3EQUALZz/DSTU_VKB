import logging
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
from app.logic.commands.images import RotateImageCommand
from app.logic.message_bus import MessageBus

router: Final[Router] = Router(name=__name__)
router.message.middleware(ProcessingMiddleware())

logger: Final[logging.Logger] = logging.getLogger(__name__)


@router.callback_query(
    AppState.IMAGE.ACTION_SELECTION,
    ImageClickActionCallback.filter(F.action == ImageCLickAction.ROTATE))  # type: ignore
async def handle_rotate_and_send_message_action(
        query: CallbackQuery,
        state: FSMContext
) -> None:
    await state.set_state(AppState.IMAGE.ROTATE_ANGLE)
    await query.message.answer("Введите угол поворота (0-360):")
    await query.answer()


@router.message(
    AppState.IMAGE.ROTATE_ANGLE,
    F.text.regexp(r"^\d+$")
)
async def handle_rotate_action(
        message: Message,
        state: FSMContext,
        bootstrap: FromDishka[Bootstrap],
) -> None:
    angle: int = int(message.text)
    image_entity: ImageEntity = (await state.get_data())["context"]
    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        RotateImageCommand(
            angle=angle,
            data=image_entity.data,
            chat_id=message.chat.id,
            width=image_entity.width,
            height=image_entity.height,
            name=image_entity.name
        )
    )

    await state.set_state(AppState.IMAGE.WAITING_PHOTO)
