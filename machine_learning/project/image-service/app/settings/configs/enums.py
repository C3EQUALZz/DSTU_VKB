from enum import StrEnum
from typing import Final


class TaskNamesConfig(StrEnum):
    RGB_TO_GRAYSCALE = "convert_rgb_to_grayscale"
    GRAYSCALE_TO_RGB = "convert_grayscale_to_rgb"
    CROP = "convert_crop"
    ROTATION = "convert_rotation"
    STYLIZATION = "convert_stylization"
