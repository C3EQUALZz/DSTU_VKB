from abc import ABC
from dataclasses import dataclass

from app.exceptions.base import BaseAppError


@dataclass(frozen=True)
class BasePresenterError(BaseAppError, ABC):
    ...
