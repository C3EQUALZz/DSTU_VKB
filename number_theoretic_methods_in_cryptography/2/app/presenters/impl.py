from typing import Iterable, override

from app.models.euler.interface import EulerModelInterface
from app.presenters.interface import PresenterInterface
from app.views.interface import ViewInterface


class EulerPresenter(PresenterInterface):
    def __init__(self, model: EulerModelInterface) -> None:
        self.model: EulerModelInterface = model
        self.view: ViewInterface | None = None

    @override
    def attach_view(self, view: ViewInterface) -> None:
        self.view: ViewInterface = view

    @override
    def calculate(self) -> None:
        if not self.view:
            return

        try:
            a: int = self.view.get_a()
            b: int = self.view.get_b()

            k: int = self.view.get_k()
            m: int = self.view.get_m()

            n: int = self.view.get_n()

            print(f"{a=}, {b=}, {k=}, {m=}, {n=}")

            # Вычисляем результаты для первого и второго чисел
            result1 = self.model.solve_congruence(a=a, b=b, n=n)
            print(result1)

            result2 = self.model.solve_congruence(a=k, b=m, n=n)
            print(result2)

            sum_result = (result1 + result2) % n

            # Обновляем view
            self.view.set_result1(f"{result1}")
            self.view.set_result2(f"{result2}")
            self.view.set_sum_result(f"{sum_result}")

            # Получаем логи из модели
            logs: Iterable[str] = self.model.get_logs()
            self.view.show_logs(logs)

        except ValueError as e:
            self.view.show_error(str(e))
