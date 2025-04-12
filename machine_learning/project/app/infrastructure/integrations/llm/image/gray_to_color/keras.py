from typing import override

from app.infrastructure.integrations.llm.image.gray_to_color.base import BaseImageColorizationModel


class KerasImageColorizationModel(BaseImageColorizationModel):
    def __init__(self, model) -> None:
        ...

    @override
    async def preprocess(self, input_data: bytes) -> np.ndarray[bytes]:
        """Препроцессинг входных данных"""
        raise NotImplementedError

    @override
    async def predict(self, processed_data: np.ndarray[bytes]) -> np.ndarray[bytes]:
        """Выполнение предсказания"""
        raise NotImplementedError

    @override
    async def postprocess(self, prediction: np.ndarray[bytes]) -> bytes:
        """
        Постобработка результатов
        """
        raise NotImplementedError
