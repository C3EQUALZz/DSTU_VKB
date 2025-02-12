from app.domain.entities.base import BaseEntity
from dataclasses import dataclass


@dataclass(eq=False)
class MathExpression(BaseEntity):
    data: str

