from typing import override

from app.exceptions.presenters.system_of_comprasion_of_the_first_degree import ComparisonSystemIsIncompatible, \
    ValidationInputError
from app.models.system_of_comprasion_of_the_first_degree.base import IChineseRemainderSolver
from app.models.system_of_comprasion_of_the_first_degree.impl import ChineseRemainderSolver
from app.presenters.tasks.system_of_comprasion_of_the_first_degree.base import ICRTPresenter
from app.views.tasks.system_of_comprasion_of_the_first_degree.base import ICRTView


class CRTPresenter(ICRTPresenter):
    def __init__(self) -> None:
        self._model: IChineseRemainderSolver = ChineseRemainderSolver()
        self._view: ICRTView | None = None

    @override
    def attach_view(self, view: ICRTView) -> None:
        self._view: ICRTView = view

    @override
    def on_activate(self) -> None:
        """Вызывается при активации презентера"""
        if self._view is None:
            ...

    @override
    def solve_system(self) -> None:
        try:
            # Получаем данные из View
            b_values = [int(val) for val in self._view.get_remainders()]
            m_values = [int(val) for val in self._view.get_moduli()]
            c_values = [int(val) for val in self._view.get_coefficients()]

            # Обновляем View
            if self._model.solve(b_values, m_values, c_values):
                self._view.show_logs(self._model.get_logs())
            else:
                raise ComparisonSystemIsIncompatible("Система сравнений несовместна")
        except ValueError:
            raise ValidationInputError("Введите целые числа")
