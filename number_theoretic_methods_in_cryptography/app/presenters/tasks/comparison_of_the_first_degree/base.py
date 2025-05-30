from typing import Protocol

from app.presenters.tasks.base import ITaskPresenter


class IComparisonOfFirstDegreePresenter(ITaskPresenter[], Protocol):
    def solve_congruence(self) -> None:
        raise NotImplementedError
