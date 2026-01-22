from dataclasses import dataclass
from uuid import UUID

from typing_extensions import override

from vulnfinder.domain.common.errors import DomainFieldError
from vulnfinder.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True)
class ContextBundleId(BaseValueObject):
    value: UUID

    @override
    def _validate(self) -> None:
        if not isinstance(self.value, UUID):
            msg = "ContextBundleId must be a UUID."
            raise DomainFieldError(msg)

    @override
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, eq=True)
class RetrievedDocumentId(BaseValueObject):
    value: UUID

    @override
    def _validate(self) -> None:
        if not isinstance(self.value, UUID):
            msg = "RetrievedDocumentId must be a UUID."
            raise DomainFieldError(msg)

    @override
    def __str__(self) -> str:
        return str(self.value)
