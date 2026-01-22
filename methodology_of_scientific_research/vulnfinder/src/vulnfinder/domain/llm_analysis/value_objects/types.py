from dataclasses import dataclass

from vulnfinder.domain.common.errors import DomainFieldError
from vulnfinder.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True)
class ModelName(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not self.value.strip():
            msg = "ModelName cannot be blank."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, eq=True)
class Prompt(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not self.value.strip():
            msg = "Prompt cannot be blank."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, eq=True)
class Temperature(BaseValueObject):
    value: float

    def _validate(self) -> None:
        if not 0.0 <= self.value <= 2.0:
            msg = "Temperature must be between 0 and 2."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return f"{self.value:.2f}"


@dataclass(frozen=True, eq=True)
class TokenUsage(BaseValueObject):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    def _validate(self) -> None:
        if self.prompt_tokens < 0 or self.completion_tokens < 0 or self.total_tokens < 0:
            msg = "Token counts must be non-negative."
            raise DomainFieldError(msg)

        if self.total_tokens != self.prompt_tokens + self.completion_tokens:
            msg = "total_tokens must equal prompt_tokens + completion_tokens."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return f"total={self.total_tokens}"
