from abc import ABC
from dataclasses import dataclass

from app.exceptions.base import BaseAppError


@dataclass(eq=False)
class ApplicationError(BaseAppError, ABC):
    ...

