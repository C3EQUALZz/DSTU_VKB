from app.exceptions.presenters.legendre_and_jacobi_symbols import DenominatorsMustBePositiveNumbers, \
    MustWriteNumbersOnlyError
from app.models.legendre_and_jacobi_symbols.base import ILegendreJacobiModel
from app.models.legendre_and_jacobi_symbols.impl import LegendreJacobiModel
from app.presenters.tasks.legendre_and_jacobi_symbols.base import ILegendreJacobiPresenter
from app.views.tasks.legendre_and_jacobi_symbols.base import ILegendreJacobiView
from typing import override


class LegendreJacobiPresenter(ILegendreJacobiPresenter):
    def __init__(self) -> None:
        self._view: ILegendreJacobiView | None = None
        self._model: ILegendreJacobiModel = LegendreJacobiModel()

    @override
    def attach_view(self, view: ILegendreJacobiView) -> None:
        self._view: ILegendreJacobiView = view

    @override
    def on_activate(self) -> None:
        """Вызывается при активации презентера"""
        if not self._view:
            raise ValueError()

    @override
    def calculate(self) -> None:
        try:
            a1: int = int(self._view.get_a1())
            b1: int = int(self._view.get_b1())
            a2: int = int(self._view.get_a2())
            b2: int = int(self._view.get_b2())
        except ValueError:
            raise MustWriteNumbersOnlyError("Введите целые числа, а не какие-то другие")

        if b1 <= 0 or b2 <= 0:
            raise DenominatorsMustBePositiveNumbers("Знаменатели должны быть положительными числами")

        numerator: int = a1 * a2
        denominator: int = b1 * b2

        # Символ Лежандра
        legendre_result: int = self._model.calculate_legendre(numerator, denominator)
        self._view.set_legendre_result(legendre_result)
        self._view.set_legendre_logs(self._model.get_legendre_logs())

        # Символ Якоби
        jacobi_result: int = self._model.calculate_jacobi(numerator, denominator)
        self._view.set_jacobi_result(jacobi_result)
        self._view.set_jacobi_logs(self._model.get_jacobi_logs())
