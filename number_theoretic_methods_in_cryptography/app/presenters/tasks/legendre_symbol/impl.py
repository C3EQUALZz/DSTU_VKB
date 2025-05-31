from typing import override

from app.exceptions.presenters.legendre_symbols import NumbersMustBeInteger
from app.models.legendre_symbol.base import ILegendreModel
from app.models.legendre_symbol.impl import LegendreModel
from app.presenters.tasks.legendre_symbol.base import ILegendrePresenter
from app.views.tasks.legendre_symbol.base import ILegendreView


class LegendrePresenter(ILegendrePresenter):
    def __init__(self) -> None:
        self._model: ILegendreModel = LegendreModel()
        self._view: ILegendreView | None = None

    @override
    def attach_view(self, view: ILegendreView) -> None:
        self._view: ILegendreView = view

    @override
    def on_activate(self) -> None:
        """Вызывается при активации презентера"""
        if not self._view:
            raise RuntimeError(f"Не привязан view к классу {self.__class__.__name__}")

    @override
    def calculate(self) -> None:
        try:
            variant_number: int = int(self._view.get_variant_number())

            # Генерация n и p
            n, p = self._model.generate_n_p(variant_number)
            self._view.set_n(n)
            self._view.set_p(p)

            # Вычисление символа Лежандра
            legendre_result: int = self._model.calculate_legendre(n, p)
            self._view.set_legendre_result(n=n, p=p, result=legendre_result)
            self._view.set_logs(self._model.get_logs())

        except ValueError:
            raise NumbersMustBeInteger("Введите целое число для варианта")
