from dataclasses import dataclass

from typing_extensions import override

from chat_service.domain.common.values.base import BaseValueObject
from chat_service.domain.user.errors import BadAPIKeyError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class OpenRouterAPIKey(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if (
                self.value.isspace()
                or self.value.isdigit()
                or self.value.isalpha()
        ):
            msg = "api key is bad"
            raise BadAPIKeyError(msg)

    @override
    def __str__(self) -> str:
        return str(self.value)
