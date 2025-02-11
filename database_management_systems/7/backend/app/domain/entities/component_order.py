from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.entities.component import Component
from app.domain.entities.order_fullillment import OrderFulfillmentEntity


@dataclass(eq=False)
class ComponentOrderEntity(BaseEntity):
    component: Component
    order_fulfillment: OrderFulfillmentEntity

    __eq__ = BaseEntity.__eq__
    __hash__ = BaseEntity.__hash__
