from abc import ABC, abstractmethod

from app.domain.entities.image import ImageEntity


class BaseImageColorToCrayScaleConverter(ABC):
    @abstractmethod
    def convert(self, image: ImageEntity) -> ImageEntity:
        raise NotImplementedError
