from typing import override

from app.exceptions.presenters.continued_fractions import NumberCanNotBeNegative, InputMustBeNumber
from app.models.continued_fractions.base import IContinuedFractionModel
from app.models.continued_fractions.impl import ContinuedFractionModel
from app.presenters.tasks.continued_fractions.base import IContinuedFractionPresenter
from app.views.tasks.continued_fractions.base import IContinuedFractionView


class ContinuedFractionPresenter(IContinuedFractionPresenter):
    def __init__(self) -> None:
        self._model: IContinuedFractionModel = ContinuedFractionModel()
        self._view: IContinuedFractionView | None = None

    @override
    def attach_view(self, view: IContinuedFractionView) -> None:
        self._view: IContinuedFractionView = view

    @override
    def on_activate(self) -> None:
        """Вызывается при активации презентера"""
        if not self._view:
            raise RuntimeError("View не установлен")

    @override
    def calculate(self) -> None:
        try:
            a = int(self._view.get_a())
            b = int(self._view.get_b())
            m = int(self._view.get_m())

            if m <= 0:
                raise NumberCanNotBeNegative("Модуль m должен быть положительным")

            solution: int = self._model.solve_linear_congruence(a, b, m)
            self._view.set_solution(solution)
            self._view.set_logs(self._model.get_logs())

        except ValueError:
            raise InputMustBeNumber("Вводите число, а не что-то другое")
