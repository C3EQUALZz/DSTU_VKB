from typing import Final

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const

from cryptography_methods.presentation.bot.handlers.atbash.dialogs.encryption.callbacks import (
    encrypt_atbash_handler
)
from cryptography_methods.presentation.bot.handlers.atbash.dialogs.encryption.states import EncryptAtbashDialogStates

ENCRYPT_ATBASH_DIALOG: Final[Dialog] = Dialog(
    Window(
        Const("Пришлите сообщение для шифрования"),
        MessageInput(
            encrypt_atbash_handler,
            content_types=[ContentType.TEXT]
        ),
        state=EncryptAtbashDialogStates.ASK_TEXT,
    ),
)
