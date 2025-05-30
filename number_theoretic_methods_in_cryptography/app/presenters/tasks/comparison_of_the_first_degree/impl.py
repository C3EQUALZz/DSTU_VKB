from app.exceptions.presenters.comprasion_first_degree import BadInputDataFromUser
from app.models.comparison_of_the_first_degree.impl import ILinearCongruenceSolver, LinearCongruenceSolver
from app.views.tasks.comparison_of_the_first_degree.base import IComparisonOfFirstDegreeView
from typing import override, Final

from app.presenters.tasks.comparison_of_the_first_degree.base import IComparisonOfFirstDegreePresenter


class ComparisonOfFirstDegreePresenter(IComparisonOfFirstDegreePresenter):
    def __init__(self) -> None:
        self._model: Final[ILinearCongruenceSolver] = LinearCongruenceSolver()
        self._view: IComparisonOfFirstDegreeView | None = None

    @override
    def attach_view(self, view: IComparisonOfFirstDegreeView) -> None:
        self._view: IComparisonOfFirstDegreeView = view

    @override
    def solve_congruence(self) -> None:
        try:
            a: int = int(self._view.get_a())
            b: int = int(self._view.get_b())
            m: int = int(self._view.get_m())
            self._model.solve(a, b, m)
            self._view.show_logs(self._model.get_logs())
        except ValueError:
            raise BadInputDataFromUser("Введите целые числа")

    @override
    def on_activate(self) -> None:
        """Вызывается при активации презентера"""
        if not self._view:
            raise ValueError("View не установлен")
