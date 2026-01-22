from dataclasses import dataclass
from uuid import UUID

from vulnfinder.domain.common.errors import DomainFieldError
from vulnfinder.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True)
class AnalysisRunId(BaseValueObject):
    value: UUID

    def _validate(self) -> None:
        if not isinstance(self.value, UUID):
            msg = "AnalysisRunId must be a UUID."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, eq=True)
class AnalysisTargetId(BaseValueObject):
    value: UUID

    def _validate(self) -> None:
        if not isinstance(self.value, UUID):
            msg = "AnalysisTargetId must be a UUID."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, eq=True)
class AnalysisTaskId(BaseValueObject):
    value: UUID

    def _validate(self) -> None:
        if not isinstance(self.value, UUID):
            msg = "AnalysisTaskId must be a UUID."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return str(self.value)

