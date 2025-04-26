from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.entities.settings import SettingsEntity


@dataclass(eq=False)
class UserEntity(BaseEntity):
    chat_id: str
    settings: SettingsEntity
