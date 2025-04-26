from enum import StrEnum
from typing import Final


class TaskNamesConfig(StrEnum):
    RGB_TO_GRAYSCALE: Final[str] = "convert_rgb_to_grayscale"
    GRAYSCALE_TO_RGB: Final[str] = "convert_grayscale_to_rgb"
    CROP: Final[str] = "convert_crop"
    ROTATION: Final[str] = "convert_rotation"
