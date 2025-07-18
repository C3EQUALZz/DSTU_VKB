from typing import Final

from aiogram import Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from cryptography_methods.presentation.bot.handlers.simple_data_permutation.consts import (
    ENCRYPT_SIMPLE_DATA_PERMUTATION
)

from cryptography_methods.presentation.bot.handlers.simple_data_permutation.dialogs.start.states import (
    SimpleDataPermutationStartStates
)

router: Final[Router] = Router()


@router.message(F.text == ENCRYPT_SIMPLE_DATA_PERMUTATION)
async def cmd_encrypt_simple_data_permutation(
        _: Message,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=SimpleDataPermutationStartStates.START,
        mode=StartMode.RESET_STACK
    )
