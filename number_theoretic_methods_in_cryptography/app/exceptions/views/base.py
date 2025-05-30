from app.exceptions.base import BaseAppError
from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseViewError(BaseAppError, ABC):
    ...
