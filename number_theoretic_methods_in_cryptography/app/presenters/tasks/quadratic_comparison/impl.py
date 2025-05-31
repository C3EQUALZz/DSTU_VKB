from typing import override

from app.exceptions.presenters.quadratic_comparison import MustBeNumbersError
from app.models.quadratic_comparison.impl import QuadraticComparisonModel
from app.presenters.tasks.quadratic_comparison.base import IQuadraticComparisonPresenter
from app.views.tasks.quadratic_comparison.base import IQuadraticComparisonView


class QuadraticComparisonPresenter(IQuadraticComparisonPresenter):
    def __init__(self) -> None:
        self._model = QuadraticComparisonModel()
        self._view: IQuadraticComparisonView | None = None

    @override
    def on_activate(self) -> None:
        """Вызывается при активации презентера"""
        if self._view is None:
            raise RuntimeError("Не был вызван метод attach_view")

    @override
    def attach_view(self, view: IQuadraticComparisonView) -> None:
        """Привязывает View к Presenter'у"""
        self._view: IQuadraticComparisonView = view

    @override
    def calculate(self) -> None:
        """Обработчик нажатия на 'Вычислить'"""
        try:
            # Получаем данные из View
            number: int = int(self._view.get_number())
            prime: int = int(self._view.get_prime())

            # Решаем квадратичное сравнение
            root: tuple[int, int] = self._model.solve_quadratic_comparison(number, prime)
            self._view.set_result(root)
            self._view.show_logs(self._model.get_logs())

        except ValueError:
            raise MustBeNumbersError("Введите целые числа")
