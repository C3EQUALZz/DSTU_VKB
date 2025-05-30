from dataclasses import dataclass

from app.exceptions.models.base import BaseModelError


@dataclass(frozen=True)
class DenominatorsMustBePositiveNumbers(BaseModelError):
    ...


@dataclass(frozen=True)
class MustWriteNumbersOnlyError(BaseModelError):
    ...
