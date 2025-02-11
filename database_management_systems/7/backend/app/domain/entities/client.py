from app.domain.entities.base import BaseEntity
from dataclasses import dataclass

from app.domain.values.shared import PhoneNumber, HumanFullNameComponent


@dataclass(eq=False)
class ClientEntity(BaseEntity):
    surname: HumanFullNameComponent
    name: HumanFullNameComponent
    patronymic: HumanFullNameComponent
    number: PhoneNumber

    __eq__ = BaseEntity.__eq__
    __hash__ = BaseEntity.__hash__

