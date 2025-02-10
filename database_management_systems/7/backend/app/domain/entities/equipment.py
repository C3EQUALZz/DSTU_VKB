from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.equipment import SerialNumber, NameOfEquipment, ModelOfEquipment


@dataclass(eq=False)
class EquipmentEntity(BaseEntity):
    """
    This represents a single equipment entity. It has several attributes:
    - name: name of the equipment, for example "Motherboard ASUS".
    - serial_number: serial number of the equipment, for example "0123456789".
    - model: model of the equipment. For example "GT710"
    """
    name: NameOfEquipment
    serial_number: SerialNumber
    model: ModelOfEquipment

    __eq__ = BaseEntity.__eq__
    __hash__ = BaseEntity.__hash__