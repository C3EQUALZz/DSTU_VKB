from aiogram import Dispatcher

from compressor.presentation.telegram.handlers.start.dialogs import START_DIALOG
from compressor.presentation.telegram.handlers.start.handler import router as start_router


def setup_start_handlers(dp: Dispatcher) -> None:
    dp.include_router(start_router)


def setup_start_dialogs(dp: Dispatcher) -> None:
    dp.include_router(START_DIALOG)
