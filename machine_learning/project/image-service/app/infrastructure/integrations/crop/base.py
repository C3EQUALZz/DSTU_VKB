from abc import ABC, abstractmethod

from app.domain.entities.image import ImageEntity


class BaseImageCropConverter(ABC):
    @abstractmethod
    def convert(self, image: ImageEntity, new_width: int, new_height: int) -> ImageEntity:
        raise NotImplementedError
