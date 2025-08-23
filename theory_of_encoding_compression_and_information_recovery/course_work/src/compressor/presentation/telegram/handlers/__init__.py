from aiogram import Dispatcher

from compressor.presentation.telegram.handlers.common import setup_common_handlers
from compressor.presentation.telegram.handlers.compress import setup_compress_handlers, setup_compress_dialogs
from compressor.presentation.telegram.handlers.start import setup_start_handlers, setup_start_dialogs


def setup_all_handlers(dp: Dispatcher) -> None:
    setup_compress_handlers(dp)
    setup_common_handlers(dp)
    setup_start_handlers(dp)


def setup_all_dialogs(dp: Dispatcher) -> None:
    setup_compress_dialogs(dp)
    setup_start_dialogs(dp)

