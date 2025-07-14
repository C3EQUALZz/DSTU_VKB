from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def on_click_encryption(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager
) -> None:
    await manager.start()


async def on_click_decryption(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager
) -> None:
    await manager.start()
