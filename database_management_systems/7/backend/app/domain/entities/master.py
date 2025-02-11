from datetime import date

from app.domain.entities.base import BaseEntity
from dataclasses import dataclass

from app.domain.values.master import PositionOfMaster
from app.domain.values.shared import HumanFullNameComponent, PhoneNumber


@dataclass(eq=False)
class MasterEntity(BaseEntity):
    """
    Domain entity that represents the master.
    It has several attributes:
    - position: it's position of a master, the same as the name of the job. For example, plumber.
    - surname: usual human surname.
    - name: usual human name.
    - patronymic: usual human patronymic.
    - address: his place of work.
    - number: his work phone number, which you can call him.
    - date_of_employment: the day the master came to work at all.
    """
    position: PositionOfMaster
    surname: HumanFullNameComponent
    name: HumanFullNameComponent
    patronymic: HumanFullNameComponent
    address: str
    number: PhoneNumber
    date_of_employment: date

    __eq__ = BaseEntity.__eq__
    __hash__ = BaseEntity.__hash__