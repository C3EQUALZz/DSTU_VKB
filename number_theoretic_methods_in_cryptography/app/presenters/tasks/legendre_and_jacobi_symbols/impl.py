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
            numerator: int = int(self._view.get_numerator())
            denominator: int = int(self._view.get_denominator())
        except ValueError:
            raise MustWriteNumbersOnlyError("Введите целые числа, а не какие-то другие")

        if denominator <= 0:
            raise DenominatorsMustBePositiveNumbers("Знаменатель должен быть положительным числом")

        # Определяем тип символа на основе знаменателя
        if self._is_prime(denominator):
            # Если знаменатель простое число - вычисляем символ Лежандра
            symbol_type = "Лежандра"
            try:
                result: int = self._model.calculate_legendre(numerator, denominator)
                self._view.set_result(symbol_type, result if result != -2 else "Невозможно посчитать")
                self._view.set_logs(self._model.get_legendre_logs())
            except Exception as e:
                self._view.set_result(symbol_type, f"Ошибка: {str(e)}")
                self._view.set_logs([f"Ошибка вычисления символа Лежандра: {str(e)}"])
        else:
            # Если знаменатель составное число - вычисляем символ Якоби
            symbol_type = "Якоби"
            try:
                result: int = self._model.calculate_jacobi(numerator, denominator)
                self._view.set_result(symbol_type, result)
                self._view.set_logs(self._model.get_jacobi_logs())
            except ValueError as e:
                self._view.set_result(symbol_type, f"Ошибка: {str(e)}")
                self._view.set_logs([f"Ошибка вычисления символа Якоби: {str(e)}"])

    @staticmethod
    def _is_prime(n: int) -> bool:
        """Проверяет, является ли число простым."""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
