from typing import override, cast

import cv2
import tensorflow as tf
import numpy as np
from pathlib import Path
from app.infrastructure.integrations.stylization.base import BaseImageStylizationConverter
import tensorflow_hub as hub


class KerasImageStylizationConverter(BaseImageStylizationConverter):
    def __init__(self, path_to_stylization_model: Path) -> None:
        self._model = hub.load(str(path_to_stylization_model))

    @override
    def preprocess(self, content_data: bytes, style_data: bytes) -> tuple[np.ndarray, np.ndarray]:
        content_image_array: np.ndarray = np.frombuffer(content_data, dtype=np.uint8)
        content_image: cv2.typing.MatLike = cv2.imdecode(content_image_array, cv2.IMREAD_COLOR)

        style_image_array: np.ndarray = np.frombuffer(style_data, dtype=np.uint8)
        style_image: cv2.typing.MatLike = cv2.imdecode(style_image_array, cv2.IMREAD_COLOR)

        content_image: np.ndarray = content_image.astype(np.float32)[np.newaxis, ...] / 255.
        style_image: np.ndarray = style_image.astype(np.float32)[np.newaxis, ...] / 255.

        resized_style_image = tf.image.resize(style_image, (256, 256)) # type: ignore

        return content_image, resized_style_image

    @override
    def predict(self, processed_data_content: np.ndarray, processed_data_style: np.ndarray) -> np.ndarray:
        return self._model(tf.constant(processed_data_content), tf.constant(processed_data_style))[0] # type: ignore

    @override
    def postprocess(self, prediction: np.ndarray) -> bytes:
        prediction: np.ndarray = cast("np.ndarray", np.squeeze(prediction, axis=0))
        prediction: np.ndarray = cast("np.ndarray", (np.clip(prediction, 0, 1) * 255).astype(np.uint8))
        _, buf = cv2.imencode(".jpg", prediction)
        return buf.tobytes()
