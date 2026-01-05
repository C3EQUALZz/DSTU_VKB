from dataclasses import dataclass

from typing_extensions import override

from chat_service.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class UserName(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        ...

    @override
    def __str__(self) -> str:
        return self.value
