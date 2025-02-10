from dataclasses import dataclass
from datetime import date
from typing import Optional

from app.domain.entities.base import BaseEntity
from app.domain.values.shared import Money


@dataclass(eq=False)
class OrderFulfillment(BaseEntity):
    type_of_work: str
    cost: Money
    cost_of_components: Optional[Money]
    fulfillment_date: date

    __eq__ = BaseEntity.__eq__
    __hash__ = BaseEntity.__hash__

    @property
    def total_cost(self) -> Money:
        return Money(self.cost.value + (self.cost_of_components if self.cost_of_components is not None else 0))