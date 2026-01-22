from dataclasses import dataclass
from uuid import UUID

from vulnfinder.domain.common.errors import DomainFieldError
from vulnfinder.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True)
class ReportId(BaseValueObject):
    value: UUID

    def _validate(self) -> None:
        if not isinstance(self.value, UUID):
            msg = "ReportId must be a UUID."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, eq=True)
class ReportItemId(BaseValueObject):
    value: UUID

    def _validate(self) -> None:
        if not isinstance(self.value, UUID):
            msg = "ReportItemId must be a UUID."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return str(self.value)

