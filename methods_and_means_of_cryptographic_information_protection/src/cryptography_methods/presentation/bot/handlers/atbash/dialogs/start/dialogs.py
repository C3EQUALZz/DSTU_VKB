from typing import Final

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Start
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const

from cryptography_methods.presentation.bot.handlers.atbash.dialogs.decryption.states import DecryptAtbashDialogStates
from cryptography_methods.presentation.bot.handlers.atbash.dialogs.encryption.states import EncryptAtbashDialogStates
from cryptography_methods.presentation.bot.handlers.atbash.dialogs.start.states import AtbashStartStates
from cryptography_methods.setup.settings import EXPLAIN_ATBASH_PATH

START_ATBASH_DIALOG: Final[Dialog] = Dialog(
    Window(
        Const("Условие представлено ниже на фотографии"),
        StaticMedia(
            path=EXPLAIN_ATBASH_PATH,
            type=ContentType.PHOTO
        ),
        Start(
            Const("Шифрование"),
            id="encrypt_atabash_button_sub_dialog",
            state=EncryptAtbashDialogStates.ASK_TEXT
        ),
        Start(
            Const("Дешифрование"),
            id="decrypt_atabash_button_sub_dialog",
            state=DecryptAtbashDialogStates.ASK_TEXT
        ),
        state=AtbashStartStates.START,
    )
)
