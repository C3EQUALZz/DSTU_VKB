from dataclasses import dataclass

from typing import override, Final

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import BadPositionOfMasterException

POSITIONS: Final[tuple[str, ...]] = (
    "Электрик",
    "Сантехник",
    "Монтажник",
    "Слесарь",
    "Механик",
    "Инженер по ремонту",
    "Техник",
    "Специалист по настройке",
    "Мастер по обслуживанию",
    "Электромеханик",
    "Радиомонтажник",
    "Автомеханик",
    "Сборщик оборудования",
    "Инженер-наладчик",
    "Инженер-конструктор"
)


@dataclass(frozen=True)
class PositionOfMaster(BaseValueObject):
    value: str

    @override
    def validate(self) -> None:
        if self.value not in POSITIONS:
            raise BadPositionOfMasterException(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
