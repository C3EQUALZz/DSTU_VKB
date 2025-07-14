from typing import Final

from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window, LaunchMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const

from cryptography_methods.presentation.bot.handlers.simple_data_permutation.dialogs.start.callbacks import (
    on_click_encryption,
    on_click_decryption
)
from cryptography_methods.presentation.bot.handlers.simple_data_permutation.dialogs.start.states import (
    SimpleDataPermutationStartStates
)
from cryptography_methods.setup.settings import EXAMPLE_SIMPLE_PERMUTATION_PATH

SIMPLE_DATA_PERMUTATION_START_DIALOG: Final[Dialog] = Dialog(
    Window(
        Const("Условие представлено ниже на фотографии"),
        StaticMedia(
            path=EXAMPLE_SIMPLE_PERMUTATION_PATH,
            type=ContentType.PHOTO
        ),
        Button(
            Const("Шифрование"),
            id="encrypt_simple_permutation_button_sub_dialog",
            on_click=on_click_encryption,
        ),
        Button(
            Const("Дешифрование"),
            id="decrypt_simple_permutation_button_sub_dialog",
            on_click=on_click_decryption,
        ),
        state=SimpleDataPermutationStartStates.START,
        launch_mode=LaunchMode.SINGLE_TOP
    ),
)
