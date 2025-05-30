from dataclasses import dataclass

from app.exceptions.models.base import BaseModelError


@dataclass(frozen=True)
class NumberOfResiduesAndModulesMustMatchError(BaseModelError):
    ...


@dataclass(frozen=True)
class InverseWasNotFoundError(BaseModelError):
    ...
