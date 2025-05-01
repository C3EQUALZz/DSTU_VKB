from abc import ABC, abstractmethod

import numpy as np


class BaseImageStylizationConverter(ABC):
    @abstractmethod
    def preprocess(self, content_data: bytes, style_data: bytes) -> tuple[np.ndarray, np.ndarray]:
        """Препроцессинг входных данных"""
        raise NotImplementedError

    @abstractmethod
    def predict(self, processed_data_content: np.ndarray, processed_data_style: np.ndarray) -> np.ndarray:
        """Выполнение предсказания"""
        raise NotImplementedError

    @abstractmethod
    def postprocess(self, prediction: np.ndarray) -> bytes:
        """
        Постобработка результатов
        """
        raise NotImplementedError

    def process(self, content_data: bytes, style_data: bytes) -> bytes:
        """Полный пайплайн обработки"""
        processed_content, processed_style = self.preprocess(content_data=content_data, style_data=style_data)
        prediction = self.predict(processed_data_content=processed_content, processed_data_style=processed_style)
        return self.postprocess(prediction)
