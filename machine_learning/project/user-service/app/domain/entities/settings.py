from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.settings import TextModel, ImageModel


@dataclass(eq=False)
class SettingsEntity(BaseEntity):
    text_model: TextModel
    image_model: ImageModel