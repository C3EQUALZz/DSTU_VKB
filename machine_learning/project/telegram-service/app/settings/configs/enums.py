from enum import Enum
from typing import Final


class TaskNamesConfig(Enum):
    SEND_CONVERTED_IMAGE_TO_USER = "send_image_to_user"
    IMAGE_METADATA = "image_metadata"
    SEND_TEXT_TO_USER = "send_text_to_user"

class TasksMiddlewareDefaultConfig(Enum):
    DEFAULT_RETRY_COUNT = 10
    DEFAULT_RETRY_DELAY = 10
    USE_JITTER = True
    USE_DELAY_EXPONENT = True
    MAX_DELAY_COMPONENT = 120
