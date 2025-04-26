from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.statistics import PositiveNumber


@dataclass(eq=False)
class StatisticsEntity(BaseEntity):
    number_of_text_request: PositiveNumber
    number_of_image_request: PositiveNumber
    number_of_voice_request: PositiveNumber
