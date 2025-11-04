from aiogram import Dispatcher

from compressor.presentation.telegram.handlers.common import setup_common_handlers
from compressor.presentation.telegram.handlers.compress import setup_compress_dialogs, setup_compress_handlers
from compressor.presentation.telegram.handlers.decompress import setup_decompress_dialogs, setup_decompress_handlers
from compressor.presentation.telegram.handlers.start import setup_start_dialogs, setup_start_handlers


def setup_all_handlers(dp: Dispatcher) -> None:
    setup_compress_handlers(dp)
    setup_common_handlers(dp)
    setup_start_handlers(dp)
    setup_decompress_handlers(dp)


def setup_all_dialogs(dp: Dispatcher) -> None:
    setup_compress_dialogs(dp)
    setup_start_dialogs(dp)
    setup_decompress_dialogs(dp)

