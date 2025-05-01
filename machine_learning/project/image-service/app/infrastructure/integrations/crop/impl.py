from typing import override

import cv2
import numpy as np

from app.domain.entities.image import ImageEntity
from app.domain.values.image import PositiveNumber
from app.exceptions.infrastructure import Cv2ImageDecodingError
from app.infrastructure.integrations.crop.base import BaseImageCropConverter


class Cv2ImageCropConverter(BaseImageCropConverter):
    @override
    def convert(self, image: ImageEntity, new_width: int, new_height: int) -> ImageEntity:
        # Преобразуем байты в массив NumPy
        buffer: np.ndarray = np.frombuffer(image.data, np.uint8)

        # Декодируем изображение
        img: cv2.typing.MatLike = cv2.imdecode(buffer, cv2.IMREAD_COLOR)

        if img is None:
            raise Cv2ImageDecodingError("Failed to decoding image")

        # Изменяем размер изображения
        resized_img: cv2.typing.MatLike = cv2.resize(img, (new_width, new_height))

        # Кодируем изображение обратно в байты
        _, buffer = cv2.imencode('.jpg', resized_img)

        return ImageEntity(
            data=buffer.tobytes(),
            width=PositiveNumber(new_width),
            height=PositiveNumber(new_height),
            name=image.name,
        )
