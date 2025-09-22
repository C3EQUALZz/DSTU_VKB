from aiogram import Dispatcher

from cryptography_methods.presentation.bot.handlers.atbash.dialogs.decryption.dialogs import DECRYPT_ATBASH_DIALOG
from cryptography_methods.presentation.bot.handlers.atbash.dialogs.encryption.dialogs import ENCRYPT_ATBASH_DIALOG
from cryptography_methods.presentation.bot.handlers.atbash.dialogs.start.dialogs import START_ATBASH_DIALOG
from cryptography_methods.presentation.bot.handlers.atbash.handlers import router as atbash_router


def setup_atbash_routers(dp: Dispatcher) -> None:
    dp.include_router(atbash_router)


def setup_atbash_dialogs(dp: Dispatcher) -> None:
    dp.include_router(START_ATBASH_DIALOG)
    dp.include_router(ENCRYPT_ATBASH_DIALOG)
    dp.include_router(DECRYPT_ATBASH_DIALOG)
