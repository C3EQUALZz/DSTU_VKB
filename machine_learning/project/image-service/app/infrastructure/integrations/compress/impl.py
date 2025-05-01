from app.domain.entities.image import ImageEntity
from app.exceptions.infrastructure import Cv2ImageDecodingError
from app.infrastructure.integrations.compress.base import BaseImageCompressConverter
from typing import override
import numpy as np
import cv2


class Cv2ImageCompressConverter(BaseImageCompressConverter):
    @override
    def convert(self, image: ImageEntity, quality: int = 90) -> ImageEntity:
        # Преобразуем байты в массив NumPy
        np_arr: np.ndarray = np.frombuffer(image.data, np.uint8)
        # Декодируем изображение
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            raise Cv2ImageDecodingError("Failed to decoding image")

        # Кодируем изображение с заданным качеством
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        _, buffer = cv2.imencode('.jpg', img, encode_param)

        return ImageEntity(
            data=buffer.tobytes(),
            width=image.width,
            height=image.height,
            name=image.name,
        )
