from typing import override

import cv2
import numpy as np

from app.domain.entities.image import ImageEntity
from app.infrastructure.integrations.color_to_gray.base import BaseImageColorToCrayScaleConverter


class Cv2ImageColorToCrayScaleConverter(BaseImageColorToCrayScaleConverter):
    @override
    def convert(self, image: ImageEntity) -> ImageEntity:
        cv2_image: cv2.typing.MatLike = cv2.imdecode(np.frombuffer(image.data, dtype=np.uint8), cv2.IMREAD_COLOR)
        gray_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)

        return ImageEntity(
            data=gray_image.tobytes(),
            width=image.width,
            height=image.height,
            name=image.name,
        )
