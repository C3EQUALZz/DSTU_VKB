from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.component import NameOfComponent
from app.domain.values.shared import Money


@dataclass(eq=False)
class Component(BaseEntity):
    name: NameOfComponent
    amount: int
    cost_per_unit: Money
