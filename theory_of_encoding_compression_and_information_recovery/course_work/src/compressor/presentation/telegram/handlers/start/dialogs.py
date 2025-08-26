from typing import Final

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Format

from compressor.presentation.telegram.handlers.start.callbacks import register_handler_callback
from compressor.presentation.telegram.handlers.start.consts import HELLO, SUCCESS_REGISTER
from compressor.presentation.telegram.handlers.start.getters import get_user_name
from compressor.presentation.telegram.handlers.start.states import StartStates
from compressor.presentation.telegram.widgets.i18n_format import I18NFormat

START_DIALOG: Final[Dialog] = Dialog(
    Window(
        I18NFormat(HELLO, username=Format("{username}")),
        MessageInput(id="password", func=register_handler_callback, content_types=[ContentType.TEXT]),
        state=StartStates.START,
        getter=get_user_name
    ),
    Window(
        I18NFormat(SUCCESS_REGISTER),
        state=StartStates.DONE,
    ),
)
