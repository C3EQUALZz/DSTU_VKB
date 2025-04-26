from abc import ABC, abstractmethod

from app.domain.entities.image import ImageEntity


class BaseImageRotationConverter(ABC):
    @abstractmethod
    def convert(self, image: ImageEntity, angle: int = 90) -> ImageEntity:
        raise NotImplementedError
