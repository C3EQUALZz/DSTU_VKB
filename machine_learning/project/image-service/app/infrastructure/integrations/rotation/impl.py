from app.domain.entities.image import ImageEntity
from app.exceptions.infrastructure import Cv2ImageDecodingError
from app.infrastructure.integrations.rotation.base import BaseImageRotationConverter
from typing import override
import numpy as np
import cv2


class Cv2ImageRotationConverter(BaseImageRotationConverter):
    @override
    def convert(self, image: ImageEntity, angle: int = 90) -> ImageEntity:
        # Преобразуем байты в массив NumPy
        np_arr: np.ndarray = np.frombuffer(image.data, np.uint8)

        # Декодируем изображение
        img: cv2.typing.MatLike = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            raise Cv2ImageDecodingError("Failed to decoding image")

        # Получаем размеры изображения
        (h, w) = img.shape[:2]

        # Находим центр изображения
        center: tuple[int, int] = (w // 2, h // 2)

        # Получаем матрицу поворота
        rotation_matrix: cv2.typing.MatLike = cv2.getRotationMatrix2D(center, angle, 1.0)

        # Поворачиваем изображение
        rotated_img: cv2.typing.MatLike = cv2.warpAffine(img, rotation_matrix, (w, h))

        # Кодируем изображение обратно в байты
        _, buffer = cv2.imencode('.jpg', rotated_img)

        return ImageEntity(
            data=buffer.tobytes(),
            width=image.width,
            height=image.height,
            name=image.name
        )
