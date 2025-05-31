from dataclasses import dataclass

from app.exceptions.models.base import BaseModelError


@dataclass(frozen=True)
class ModulusMustBeAnOddPrimeNumberError(BaseModelError):
    ...


@dataclass(frozen=True)
class NotAQuadraticDeductionError(BaseModelError):
    ...
