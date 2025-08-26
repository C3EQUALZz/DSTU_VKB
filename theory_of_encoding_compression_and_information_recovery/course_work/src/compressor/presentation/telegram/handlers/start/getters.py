import logging
from typing import Final

from aiogram.types import User
from aiogram_dialog import DialogManager

logger: Final[logging.Logger] = logging.getLogger(__name__)


async def get_user_name(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    user: User = dialog_manager.event.from_user

    logger.info("Getting user info, user: %s", user)

    return {
        "username": user.username,
    }
