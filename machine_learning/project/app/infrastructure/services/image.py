from app.domain.entities.message import ImageMessageEntity
from app.infrastructure.integrations.llm.image.gray_to_color.base import BaseImageColorizationModel


class ImageService:
    def __init__(
            self,
            colorization_model: BaseImageColorizationModel
    ) -> None:
        self._colorization_model = colorization_model

    async def convert_gray_image_to_color(self, image: ImageMessageEntity) -> ImageMessageEntity:
        self._colorization_model.
