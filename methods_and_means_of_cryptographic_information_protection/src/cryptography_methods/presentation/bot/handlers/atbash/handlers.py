from typing import Final

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from cryptography_methods.presentation.bot.filters.chat import ChatTypeFilter
from cryptography_methods.presentation.bot.handlers.atbash.dialogs.start.states import AtbashStartStates

router: Final[Router] = Router()


@router.message(
    ChatTypeFilter(allowed_chat_types=[ChatType.PRIVATE]),
    Command("atbash")
)
async def cmd_start_atbash_dialog(
        _: Message,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=AtbashStartStates.START,
        mode=StartMode.RESET_STACK
    )
