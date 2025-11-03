from aiogram import Dispatcher

from compressor.presentation.telegram.handlers.decompress.dialogs import (
    DECOMPRESS_DIALOG,
    DECOMPRESS_BINARY_OR_TEXT_FILE_DIALOG
)
from compressor.presentation.telegram.handlers.decompress.handlers import router as decompress_router


def setup_compress_handlers(dp: Dispatcher) -> None:
    dp.include_router(decompress_router)


def setup_decompress_dialogs(dp: Dispatcher) -> None:
    dp.include_router(DECOMPRESS_DIALOG)
    dp.include_router(DECOMPRESS_BINARY_OR_TEXT_FILE_DIALOG)
