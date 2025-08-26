import operator
from typing import Final

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Group, Select
from aiogram_dialog.widgets.text import Format

from compressor.presentation.telegram.handlers.compress.callbacks import (
    compress_binary_or_text_file,
    on_algorithm_selected,
)
from compressor.presentation.telegram.handlers.compress.consts import (
    ASK_FOR_BINARY_OR_TEXT_FILE,
    CHOOSE_BINARY_OR_TEXT_FILE_COMPRESSION_TYPE,
    COMPRESS_BINARY_OR_TEXT_FILE,
    COMPRESS_START,
    SELECTOR_ALGORITHM,
    STARTED_PROCESSING,
)
from compressor.presentation.telegram.handlers.compress.getters import (
    get_compression_for_binary_or_text_files,
    task_id_getter,
)
from compressor.presentation.telegram.handlers.compress.states import CompressBinaryOrTextFileStates, CompressStates
from compressor.presentation.telegram.widgets.i18n_format import I18NFormat

COMPRESS_DIALOG: Final[Dialog] = Dialog(
    Window(
        I18NFormat(COMPRESS_START),
        Group(
            Button(
                I18NFormat(COMPRESS_BINARY_OR_TEXT_FILE),
                id=COMPRESS_BINARY_OR_TEXT_FILE,
            ),
            width=1
        ),
        state=CompressStates.START,
    ),
)

COMPRESS_BINARY_OR_TEXT_FILE_DIALOG: Final[Dialog] = Dialog(
    Window(
        I18NFormat(CHOOSE_BINARY_OR_TEXT_FILE_COMPRESSION_TYPE),
        Select(
            Format("{item[0]} ({pos}/data[count]})"),
            id=SELECTOR_ALGORITHM,
            item_id_getter=operator.itemgetter(1),
            items="compressor_algorithms",
            on_click=on_algorithm_selected
        ),
        state=CompressBinaryOrTextFileStates.START,
        getter=get_compression_for_binary_or_text_files
    ),
    Window(
        I18NFormat(ASK_FOR_BINARY_OR_TEXT_FILE),
        MessageInput(compress_binary_or_text_file, content_types=[ContentType.DOCUMENT]),
        state=CompressBinaryOrTextFileStates.ASK_FILE,
    ),
    Window(
        I18NFormat(STARTED_PROCESSING),
        state=CompressBinaryOrTextFileStates.DONE,
        getter=task_id_getter
    )
)
