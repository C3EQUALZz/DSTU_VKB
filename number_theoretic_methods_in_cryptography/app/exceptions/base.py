from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseAppError(Exception, ABC):
    message: str
