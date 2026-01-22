from dataclasses import dataclass

from vulnfinder.domain.common.errors import DomainFieldError
from vulnfinder.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True)
class FilePath(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not self.value.strip():
            msg = "FilePath cannot be blank."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, eq=True)
class ProgrammingLanguage(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not self.value.strip():
            msg = "ProgrammingLanguage cannot be blank."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, eq=True)
class LineRange(BaseValueObject):
    start_line: int
    end_line: int
    start_column: int | None = None
    end_column: int | None = None

    def _validate(self) -> None:
        if self.start_line <= 0:
            msg = "start_line must be positive."
            raise DomainFieldError(msg)

        if self.end_line < self.start_line:
            msg = "end_line cannot be less than start_line."
            raise DomainFieldError(msg)

        if self.start_column is not None and self.start_column < 0:
            msg = "start_column must be >= 0."
            raise DomainFieldError(msg)

        if self.end_column is not None and self.end_column < 0:
            msg = "end_column must be >= 0."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return f"{self.start_line}:{self.end_line}"
