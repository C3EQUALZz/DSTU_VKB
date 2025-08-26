from aiogram import Dispatcher

from compressor.presentation.telegram.handlers.compress.dialogs import (
    COMPRESS_BINARY_OR_TEXT_FILE_DIALOG,
    COMPRESS_DIALOG,
)
from compressor.presentation.telegram.handlers.compress.handlers import router as compress_router


def setup_compress_handlers(dp: Dispatcher) -> None:
    dp.include_router(compress_router)


def setup_compress_dialogs(dp: Dispatcher) -> None:
    dp.include_router(COMPRESS_DIALOG)
    dp.include_router(COMPRESS_BINARY_OR_TEXT_FILE_DIALOG)
