from enum import Enum

from aiogram.filters.callback_data import CallbackData


class ImageCLickAction(str, Enum):
    gray_to_color = "gray-to-color"


class ImageClickActionCallback(CallbackData, prefix="img"):
    action: ImageCLickAction
