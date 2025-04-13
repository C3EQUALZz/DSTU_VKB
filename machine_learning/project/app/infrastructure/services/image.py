from app.domain.entities.message import ImageMessageEntity
from app.infrastructure.integrations.llm.image.gray_to_color.base import LLMImageMessageColorizationModel


class ImageService:
    def __init__(self, colorize_image_model: LLMImageMessageColorizationModel) -> None:
        self._colorize_image_model = colorize_image_model

    async def colorize_image(self, image: ImageMessageEntity) -> ImageMessageEntity:
        data: bytes = self._colorize_image_model.process(input_data=image.photo)
        return ImageMessageEntity(photo=data, chat_id=image.chat_id)
