from dataclasses import dataclass
from abc import ABC

from app.exceptions.base import BaseAppError


@dataclass(frozen=True)
class BaseModelError(BaseAppError, ABC):
    ...
