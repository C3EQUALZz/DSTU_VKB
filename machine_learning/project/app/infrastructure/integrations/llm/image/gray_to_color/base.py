from abc import ABC, abstractmethod

import numpy as np


class BaseImageColorizationModel(ABC):
    """
    Interface for model which describes work with image colorization.
    From gray to color image
    """

    @abstractmethod
    async def preprocess(self, input_data: bytes) -> np.ndarray[bytes]:
        """Препроцессинг входных данных"""
        raise NotImplementedError

    @abstractmethod
    async def predict(self, processed_data: np.ndarray[bytes]) -> np.ndarray[bytes]:
        """Выполнение предсказания"""
        raise NotImplementedError

    @abstractmethod
    async def postprocess(self, prediction: np.ndarray[bytes]) -> bytes:
        """
        Постобработка результатов
        """
        raise NotImplementedError

    async def process(self, input_data: bytes) -> bytes:
        """Полный пайплайн обработки"""
        processed = await self.preprocess(input_data)
        prediction = await self.predict(processed)
        return await self.postprocess(prediction)
