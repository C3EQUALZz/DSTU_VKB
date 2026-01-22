import re
from dataclasses import dataclass
from uuid import UUID

from vulnfinder.domain.common.errors import DomainFieldError
from vulnfinder.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True)
class KnowledgeEntryId(BaseValueObject):
    value: UUID

    def _validate(self) -> None:
        if not isinstance(self.value, UUID):
            msg = "KnowledgeEntryId must be a UUID."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, eq=True)
class CVEId(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not re.fullmatch(r"CVE-\d{4}-\d{4,}", self.value):
            msg = f"Invalid CVE id: {self.value!r}"
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, eq=True)
class CWEId(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not re.fullmatch(r"CWE-\d{1,6}", self.value):
            msg = f"Invalid CWE id: {self.value!r}"
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return self.value

