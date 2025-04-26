from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


class ImageCLickAction(StrEnum):
    GRAY_TO_COLOR = "gray-to-color"
    METADATA = "image-metadata"
    COLOR_TO_GRAY = "color-to-gray"
    ROTATE = "rotate-angle"
    CROP = "crop"


class ImageClickActionCallback(CallbackData, prefix="img"):
    action: ImageCLickAction