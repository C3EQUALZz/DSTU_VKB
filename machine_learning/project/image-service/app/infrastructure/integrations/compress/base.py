from abc import ABC, abstractmethod

from app.domain.entities.image import ImageEntity


class BaseImageCompressConverter(ABC):
    @abstractmethod
    def convert(self, image: ImageEntity, quality: int = 90) -> ImageEntity:
        raise NotImplementedError
