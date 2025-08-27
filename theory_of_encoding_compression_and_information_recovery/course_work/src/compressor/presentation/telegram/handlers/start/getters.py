import logging
from typing import Any, Final

from aiogram.types import User
from aiogram_dialog import DialogManager

from compressor.presentation.errors.telegram import UserCantBeNoneError

logger: Final[logging.Logger] = logging.getLogger(__name__)


async def get_user_name(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, str]: # noqa: ANN401, ARG001
    user: User | None = dialog_manager.event.from_user

    if user is None:
        msg: str = "User entity must be provided"
        raise UserCantBeNoneError(msg)

    logger.info("Getting user info, user: %s", user)

    return {
        "username": user.username if user.username else user.first_name,
    }
