from dataclasses import dataclass

from vulnfinder.domain.common.errors import DomainFieldError
from vulnfinder.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True)
class AnalysisStatus(BaseValueObject):
    value: str

    def _validate(self) -> None:
        allowed = {"CREATED", "RUNNING", "FINISHED", "FAILED"}
        if self.value not in allowed:
            msg = f"Invalid analysis status: {self.value!r}"
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, eq=True)
class AnalysisTargetType(BaseValueObject):
    value: str

    def _validate(self) -> None:
        allowed = {"FILE", "DIRECTORY", "REPOSITORY"}
        if self.value not in allowed:
            msg = f"Invalid analysis target type: {self.value!r}"
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, eq=True)
class AnalysisConfig(BaseValueObject):
    recursive: bool
    enable_rag: bool
    max_files: int | None = None
    model_name: str | None = None
    language_filters: tuple[str, ...] = ()

    def _validate(self) -> None:
        if self.max_files is not None and self.max_files <= 0:
            msg = "max_files must be positive when provided."
            raise DomainFieldError(msg)

        if self.model_name is not None and not self.model_name.strip():
            msg = "model_name cannot be blank."
            raise DomainFieldError(msg)

        for language in self.language_filters:
            if not language.strip():
                msg = "language_filters must not contain blank values."
                raise DomainFieldError(msg)

    def __str__(self) -> str:
        flags = "recursive" if self.recursive else "non-recursive"
        rag = "rag" if self.enable_rag else "no-rag"
        return f"{flags}, {rag}"

