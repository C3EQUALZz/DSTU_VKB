from pathlib import Path
from typing import Final, cast, override

import cv2
import numpy as np
import tensorflow as tf

from app.infrastructure.integrations.llm.image.gray_to_color.base import LLMImageMessageColorizationModel


class KerasImageMessageColorizationModel(LLMImageMessageColorizationModel):
    SIZE: Final[int] = 160

    def __init__(self, path_to_model: Path) -> None:
        self._model = tf.keras.models.load_model(path_to_model)  # type: ignore

    @override
    def preprocess(self, input_data: bytes) -> np.ndarray:
        # Декодируем изображение
        img_np = np.frombuffer(input_data, dtype=np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        # Конвертация цветового пространства
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Ресайз с сохранением пропорций
        img = self.__resize_with_padding(img)

        # Нормализация
        img = img.astype(np.float32) / 255.0

        # Добавление размерности батча
        return np.expand_dims(img, axis=0)

    def __resize_with_padding(self, img: np.ndarray) -> np.ndarray:
        h, w = img.shape[:2]
        scale: float = min(self.SIZE / h, self.SIZE / w)
        new_h: int = int(h * scale)
        new_w: int = int(w * scale)

        resized: np.ndarray[bytes] = cv2.resize(img, (new_w, new_h))
        delta_h: int = self.SIZE - new_h
        delta_w: int = self.SIZE - new_w

        top: int = delta_h // 2
        bottom: int = delta_h - top
        left: int = delta_w // 2
        right: int = delta_w - left

        return cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    @override
    def predict(self, processed_data: np.ndarray[bytes]) -> np.ndarray[bytes]:
        """Выполнение предсказания"""
        return self._model.predict(processed_data)

    @override
    def postprocess(self, prediction: np.ndarray[bytes]) -> bytes:
        """
        Постобработка результатов
        """
        prediction: np.ndarray[bytes] = cast("np.ndarray[bytes]", np.squeeze(prediction, axis=0))
        prediction: np.ndarray[bytes] = cast("np.ndarray[bytes]", (np.clip(prediction, 0, 1) * 255).astype(np.uint8))
        _, buf = cv2.imencode(".jpg", prediction)
        return buf.tobytes()
