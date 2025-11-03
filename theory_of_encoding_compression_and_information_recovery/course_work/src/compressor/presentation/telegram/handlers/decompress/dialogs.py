import operator
from typing import Final

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, Start, Select
from aiogram_dialog.widgets.text import Format

from compressor.presentation.telegram.handlers.decompress.callbacks import (
    on_algorithm_selected,
    decompress_binary_or_text_file
)
from compressor.presentation.telegram.handlers.decompress.consts import (
    DECOMPRESS_BINARY_OR_TEXT_FILE,
    DECOMPRESS_START,
    CHOOSE_BINARY_OR_TEXT_FILE_COMPRESSION_TYPE,
    SELECTOR_ALGORITHM,
    STARTED_PROCESSING,
    ASK_FOR_BINARY_OR_TEXT_FILE
)
from compressor.presentation.telegram.handlers.decompress.getters import (
    get_compression_for_binary_or_text_files,
    task_id_getter
)
from compressor.presentation.telegram.handlers.decompress.states import (
    DecompressBinaryOrTextFileStates,
    DecompressStates
)
from compressor.presentation.telegram.widgets.i18n_format import I18NFormat

DECOMPRESS_DIALOG: Final[Dialog] = Dialog(
    Window(
        I18NFormat(DECOMPRESS_START),
        Group(
            Start(
                I18NFormat(DECOMPRESS_BINARY_OR_TEXT_FILE),
                id=DECOMPRESS_BINARY_OR_TEXT_FILE,
                state=DecompressBinaryOrTextFileStates.START,
            ),
            width=1,
        ),
        state=DecompressStates.START,
    ),
)

DECOMPRESS_BINARY_OR_TEXT_FILE_DIALOG: Final[Dialog] = Dialog(
    Window(
        I18NFormat(CHOOSE_BINARY_OR_TEXT_FILE_COMPRESSION_TYPE),
        Select(
            Format("{item[0]} ({pos}/{data[count]})"),
            id=SELECTOR_ALGORITHM,
            item_id_getter=operator.itemgetter(1),
            items="compressor_algorithms",
            on_click=on_algorithm_selected
        ),
        state=DecompressBinaryOrTextFileStates.START,
        getter=get_compression_for_binary_or_text_files
    ),
    Window(
        I18NFormat(ASK_FOR_BINARY_OR_TEXT_FILE),
        MessageInput(decompress_binary_or_text_file, content_types=[ContentType.DOCUMENT]),
        state=DecompressBinaryOrTextFileStates.ASK_FILE,
    ),
    Window(
        I18NFormat(STARTED_PROCESSING),
        state=DecompressBinaryOrTextFileStates.DONE,
        getter=task_id_getter
    )
)
