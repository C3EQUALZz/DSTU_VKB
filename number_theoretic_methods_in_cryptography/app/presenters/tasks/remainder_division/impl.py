from typing import override

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
        mode = self._view.get_mode()

        try:
            n = self._view.get_n()
            if mode == "Одно выражение":
                a = self._view.get_a()
                b = self._view.get_b()
                result = self._model.solve(a, b, n)
                logs = self._model.get_logs()
                self._view.set_result1(f"{result}")
                self._view.set_result2("")
                self._view.set_sum_result("")
                self._view.show_logs(logs)
            else:
                a = self._view.get_a()
                b = self._view.get_b()
                k = self._view.get_k()
                m = self._view.get_m()
                result1 = self._model.solve(a, b, n)
                logs1 = self._model.get_logs()
                result2 = self._model.solve(k, m, n)
                logs2 = self._model.get_logs()
                total = (result1 + result2) % n
                combined_logs = list(logs1) + ["---"] + list(logs2)
                self._view.set_result1(f"{result1}")
                self._view.set_result2(f"{result2}")
                self._view.set_sum_result(f"{total}")
                self._view.show_logs(combined_logs)

        except ValueError as e:
            self._view.show_error(str(e))
