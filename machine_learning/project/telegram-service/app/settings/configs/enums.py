from enum import Enum
from typing import Final


class TaskNamesConfig(Enum):
    SEND_CONVERTED_IMAGE_TO_USER: Final[str] = "send_image_to_user"
    IMAGE_METADATA: Final[str] = "image_metadata"
