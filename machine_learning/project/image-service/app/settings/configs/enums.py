from enum import StrEnum, Enum


class TaskNamesConfig(StrEnum):
    RGB_TO_GRAYSCALE = "convert_rgb_to_grayscale"
    GRAYSCALE_TO_RGB = "convert_grayscale_to_rgb"
    CROP = "convert_crop"
    ROTATION = "convert_rotation"
    STYLIZATION = "convert_stylization"
    INVERSION = "convert_inversion"


class TasksMiddlewareDefaultConfig(Enum):
    DEFAULT_RETRY_COUNT = 10
    DEFAULT_RETRY_DELAY = 10
    USE_JITTER = True
    USE_DELAY_EXPONENT = True
    MAX_DELAY_COMPONENT = 120
