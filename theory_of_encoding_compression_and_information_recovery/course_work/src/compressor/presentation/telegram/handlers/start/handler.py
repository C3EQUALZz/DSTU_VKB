from typing import Final

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from compressor.presentation.telegram.filters.chat import ChatTypeFilter
from compressor.presentation.telegram.handlers.start.states import StartStates

router: Final[Router] = Router()


@router.message(
    ChatTypeFilter(allowed_chat_types=[ChatType.PRIVATE]),
    CommandStart()
)
async def cmd_start_handler(
        _: Message,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=StartStates.START,
        mode=StartMode.RESET_STACK
    )
