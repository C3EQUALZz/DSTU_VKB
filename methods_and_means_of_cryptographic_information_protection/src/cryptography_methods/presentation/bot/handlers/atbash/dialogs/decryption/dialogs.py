from typing import Final

from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const

from cryptography_methods.presentation.bot.handlers.atbash.dialogs.decryption.callbacks import (
    decrypt_atbash_handler
)
from cryptography_methods.presentation.bot.handlers.atbash.dialogs.decryption.states import DecryptAtbashDialogStates

DECRYPT_ATBASH_DIALOG: Final[Dialog] = Dialog(
    Window(
        Const("Пришлите сообщение для дешифрования"),
        MessageInput(
            decrypt_atbash_handler,
            content_types=[ContentType.TEXT]
        ),
        state=DecryptAtbashDialogStates.ASK_TEXT,
    ),
)
