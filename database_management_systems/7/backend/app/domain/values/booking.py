from dataclasses import dataclass
from typing import override, Final

from app.domain.values.base import BaseValueObject

STATES: Final[tuple[str, ...]] = (
    "Принято в работу",
    "В процессе ремонта",
    "Ожидание запчастей",
    "Завершено",
    "Готово к выдаче",
    "Неисправность подтверждена",
    "Ожидание подтверждения",
    "Отказ от ремонта",
    "Закрыто"
)


@dataclass(frozen=True)
class StatusOfBooking(BaseValueObject):
    value: str

    @override
    def validate(self) -> None:
        if self.value not in STATES:
            ...

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
