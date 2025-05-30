from dataclasses import dataclass

from app.exceptions.models.base import BaseModelError


@dataclass(frozen=True)
class ComparisonSystemIsIncompatible(BaseModelError):
    ...


@dataclass(frozen=True)
class ValidationInputError(BaseModelError):
    ...
