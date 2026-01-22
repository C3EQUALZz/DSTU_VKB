from dataclasses import dataclass
from uuid import UUID

from typing_extensions import override

from vulnfinder.domain.common.errors import DomainFieldError
from vulnfinder.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True)
class CodeArtifactId(BaseValueObject):
    value: UUID

    @override
    def _validate(self) -> None:
        if not isinstance(self.value, UUID):
            msg = "CodeArtifactId must be a UUID."
            raise DomainFieldError(msg)

    @override
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, eq=True)
class CodeSnippetId(BaseValueObject):
    value: UUID

    @override
    def _validate(self) -> None:
        if not isinstance(self.value, UUID):
            msg = "CodeSnippetId must be a UUID."
            raise DomainFieldError(msg)

    @override
    def __str__(self) -> str:
        return str(self.value)
