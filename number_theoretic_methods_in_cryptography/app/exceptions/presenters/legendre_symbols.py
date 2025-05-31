from dataclasses import dataclass

from app.exceptions.presenters.base import BasePresenterError


@dataclass(frozen=True)
class NumbersMustBeInteger(BasePresenterError):
    ...
