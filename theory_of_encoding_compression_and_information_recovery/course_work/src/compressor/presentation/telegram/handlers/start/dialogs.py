from typing import Final

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const

from compressor.presentation.telegram.handlers.start.callbacks import register_handler_callback
from compressor.presentation.telegram.handlers.start.consts import HELLO
from compressor.presentation.telegram.handlers.start.getters import get_user_name
from compressor.presentation.telegram.handlers.start.states import StartStates
from compressor.presentation.telegram.widgets.i18n_format import I18NFormat

START_DIALOG: Final[Dialog] = Dialog(
    Window(
        I18NFormat(HELLO),
        state=StartStates.START,
        getter=get_user_name
    ),
    Window(
        Const("Enter your password:"),
        MessageInput(id="password", func=register_handler_callback),
        state=StartStates.ANSWER_FOR_PASSWORD,
    ),
    Window(
        Const("You are successfully registered! Type /help to see the commands"),
        state=StartStates.DONE,
    ),
)
