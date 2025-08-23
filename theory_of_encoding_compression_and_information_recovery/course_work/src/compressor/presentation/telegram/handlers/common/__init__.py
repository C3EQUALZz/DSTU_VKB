from aiogram import Dispatcher

from compressor.presentation.telegram.handlers.common.help import router as help_router
from compressor.presentation.telegram.handlers.common.me import router as me_router


def setup_common_handlers(dp: Dispatcher) -> None:
    dp.include_router(me_router)
    dp.include_router(help_router)
