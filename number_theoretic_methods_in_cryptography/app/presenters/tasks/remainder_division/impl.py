from typing import Iterable, override

from app.models.remainder_division.base import IRemainderDivision
from app.models.remainder_division.impl import EulerFermatModel
from app.presenters.tasks.remainder_division.base import IRemainderDivisionPresenter
from app.views.tasks.remainder_division.base import IRemainderDivisionView


class RemainderDivisionPresenter(IRemainderDivisionPresenter):
    def __init__(self) -> None:
        self._model: IRemainderDivision = EulerFermatModel()
        self._view: IRemainderDivisionView | None = None

    @override
    def attach_view(self, view: IRemainderDivisionView) -> None:
        self._view: IRemainderDivisionView = view

    @override
    def on_activate(self) -> None:
        """Вызывается при активации презентера"""
        if not self._view:
            raise ValueError("View не установлен")

    @override
    def calculate(self) -> None:
        if not self._view:
            return

        self._view.clear_logs()

        try:
            a: int = self._view.get_a()
            b: int = self._view.get_b()

            k: int = self._view.get_k()
            m: int = self._view.get_m()

            n: int = self._view.get_n()

            # Вычисляем результаты для первого и второго чисел
            result1 = self._model.solve(a=a, exponent=b, modulus=n)

            result2 = self._model.solve(a=k, exponent=m, modulus=n)

            sum_result = (result1 + result2) % n

            # Обновляем _view
            self._view.set_result1(f"{result1}")
            self._view.set_result2(f"{result2}")
            self._view.set_sum_result(f"{sum_result}")

            # Получаем логи из модели
            logs: Iterable[str] = self._model.get_logs()
            self._view.show_logs(logs)

        except ValueError as e:
            self._view.show_error(str(e))
