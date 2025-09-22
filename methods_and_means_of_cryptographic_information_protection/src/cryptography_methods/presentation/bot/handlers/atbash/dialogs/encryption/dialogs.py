from typing import Final

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from cryptography_methods.presentation.bot.handlers.atbash.dialogs.encryption.callbacks import (
    encrypt_atbash_error, encrypt_atbash_handler
)
from cryptography_methods.presentation.bot.handlers.atbash.dialogs.encryption.states import EncryptAtbashDialogStates

ENCRYPT_ATBASH_DIALOG: Final[Dialog] = Dialog(
    Window(
        Const("Пришлите сообщение для шифрования"),
        TextInput(
            id="encrypt_atbash_text",
            on_error=encrypt_atbash_error,
            on_success=encrypt_atbash_handler,
            type_factory=str,
        ),
        state=EncryptAtbashDialogStates.ASK_TEXT,
    ),
)
