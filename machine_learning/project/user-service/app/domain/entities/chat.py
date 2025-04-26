from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.entities.settings import SettingsEntity
from app.domain.entities.statistic import StatisticsEntity
from app.domain.entities.user import UserEntity


@dataclass(eq=False)
class PersonalChatEntity(BaseEntity):
    user: UserEntity
    settings: SettingsEntity
    statistics: StatisticsEntity
