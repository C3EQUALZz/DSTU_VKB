from abc import ABC, abstractmethod

import numpy as np


class BaseImageGrayScaleToColorConverter(ABC):
    """
    Interface for model which describes work with image colorization.
    From gray to color image
    """

    @abstractmethod
    def preprocess(self, input_data: bytes) -> np.ndarray:
        """Препроцессинг входных данных"""
        raise NotImplementedError

    @abstractmethod
    def predict(self, processed_data: np.ndarray) -> np.ndarray:
        """Выполнение предсказания"""
        raise NotImplementedError

    @abstractmethod
    def postprocess(self, prediction: np.ndarray) -> bytes:
        """
        Постобработка результатов
        """
        raise NotImplementedError

    def process(self, input_data: bytes) -> bytes:
        """Полный пайплайн обработки"""
        processed = self.preprocess(input_data)
        prediction = self.predict(processed)
        return self.postprocess(prediction)
