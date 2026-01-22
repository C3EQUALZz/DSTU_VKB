from dataclasses import dataclass

from vulnfinder.domain.common.errors import DomainFieldError
from vulnfinder.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True)
class ReportFormat(BaseValueObject):
    value: str

    def _validate(self) -> None:
        allowed = {"TEXT", "JSON", "SARIF"}
        if self.value not in allowed:
            msg = f"Invalid report format: {self.value!r}"
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, eq=True)
class ReportSummary(BaseValueObject):
    total: int
    critical: int
    high: int
    medium: int
    low: int

    def _validate(self) -> None:
        counts = (self.critical, self.high, self.medium, self.low)
        if any(value < 0 for value in counts):
            msg = "Severity counts must be non-negative."
            raise DomainFieldError(msg)

        if self.total < 0:
            msg = "Total must be non-negative."
            raise DomainFieldError(msg)

        if self.total != sum(counts):
            msg = "Total must equal sum of severity counts."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return f"total={self.total}"
