from dataclasses import dataclass
from datetime import date

from app.domain.entities.base import BaseEntity
from app.domain.entities.client import ClientEntity
from app.domain.entities.component_order import ComponentOrderEntity
from app.domain.entities.equipment import EquipmentEntity
from app.domain.entities.master import MasterEntity
from app.domain.values.booking import StatusOfBooking


@dataclass(eq=False)
class BookingEntity(BaseEntity):
    """
    Booking entity for a client.
    In our case, here consumers order the repair of their belongings.
    For example, client brings motherboard for repair. This will be our booking
    """
    equipment: EquipmentEntity
    client: ClientEntity
    master: MasterEntity
    status: StatusOfBooking
    component_order: ComponentOrderEntity
    booking_date: date

    __eq__ = BaseEntity.__eq__
    __hash__ = BaseEntity.__hash__
