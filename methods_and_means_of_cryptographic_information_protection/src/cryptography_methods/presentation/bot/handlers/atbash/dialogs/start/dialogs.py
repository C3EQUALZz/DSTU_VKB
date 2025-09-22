from typing import Final

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const

from cryptography_methods.presentation.bot.handlers.atbash.dialogs.decryption.states import DecryptAtbashDialogStates
from cryptography_methods.presentation.bot.handlers.atbash.dialogs.encryption.states import EncryptAtbashDialogStates
from cryptography_methods.presentation.bot.handlers.atbash.dialogs.start.states import AtabashStartStates

START_ATBASH_DIALOG: Final[Dialog] = Dialog(
    Window(
        Const("Условие представлено ниже на фотографии"),
        StaticMedia(
            path=...,
            type=ContentType.PHOTO
        ),
        SwitchTo(
            Const("Шифрование"),
            id="encrypt_atabash_button_sub_dialog",
            state=EncryptAtbashDialogStates.ASK_TEXT
        ),
        SwitchTo(
            Const("Дешифрование"),
            id="decrypt_atabash_button_sub_dialog",
            state=DecryptAtbashDialogStates.ASK_TEXT
        ),
        state=AtabashStartStates.START,
    )
)
