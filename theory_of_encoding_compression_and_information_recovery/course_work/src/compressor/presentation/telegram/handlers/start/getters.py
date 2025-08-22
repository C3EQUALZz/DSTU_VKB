from aiogram.types import User
from aiogram_dialog import DialogManager


async def get_user_name(dialog_manager: DialogManager,**kwargs) -> dict[str, str]:
    user: User = dialog_manager.event.from_user
    return {
        "username": user.username,
    }
