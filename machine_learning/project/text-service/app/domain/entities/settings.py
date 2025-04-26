from dataclasses import dataclass

from app.domain.entities.base import BaseEntity


@dataclass(eq=False)
class SettingsEntity(BaseEntity):
    text_model: str
