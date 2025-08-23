from typing import Final

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from compressor.presentation.telegram.filters.chat import ChatTypeFilter
from compressor.presentation.telegram.handlers.compress.states import CompressStates

router: Final[Router] = Router()


@router.message(
    ChatTypeFilter(allowed_chat_types=[ChatType.PRIVATE]),
    Command("compress")
)
async def cmd_compress_handler(
        _: Message,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=CompressStates.START,
        mode=StartMode.RESET_STACK
    )
