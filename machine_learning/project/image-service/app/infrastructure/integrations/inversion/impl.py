from typing import override

import cv2
import numpy as np

from app.domain.entities.image import ImageEntity
from app.infrastructure.integrations.inversion.base import BaseImageInversionConverter


class Cv2ImageInversionConverter(BaseImageInversionConverter):
    @override
    def convert(self, image: ImageEntity) -> ImageEntity:
        # Декодируем байты в изображение OpenCV
        np_arr = np.frombuffer(image.data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Инвертируем изображение
        inverted_img = cv2.bitwise_not(img)

        # Кодируем обратно в байты
        _, encoded_img = cv2.imencode('.png', inverted_img)
        inverted_data = encoded_img.tobytes()

        # Создаем новый объект ImageEntity
        return ImageEntity(
            data=inverted_data,
            width=image.width,
            height=image.height,
            name=image.name
        )
