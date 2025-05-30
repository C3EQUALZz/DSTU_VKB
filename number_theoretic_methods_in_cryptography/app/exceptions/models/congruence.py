from app.exceptions.models.base import BaseModelError
from dataclasses import dataclass


@dataclass(frozen=True)
class NoSolutionSinceGCDDoesNotShareFreeTermError(BaseModelError):
    ...


@dataclass(frozen=True)
class ReverseElementWasNotFound(BaseModelError):
    ...
