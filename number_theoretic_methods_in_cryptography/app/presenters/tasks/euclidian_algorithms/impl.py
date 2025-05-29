from app.models.euclidian_algorithms.base import BaseGCDStrategy, ResultDTO
from app.models.euclidian_algorithms.bezout import GCDBezout
from app.models.euclidian_algorithms.binary import GCDBinary
from app.models.euclidian_algorithms.classic import GCDMod
from app.presenters.tasks.base import ITaskPresenter
from app.presenters.tasks.euclidian_algorithms.base import IGCDPresenter
from app.presenters.tasks.euclidian_algorithms.context import AlgorithmStrategyContext
from app.views.tasks.euclidian_algorithms.base import IGCDView


class GCDCalculatorPresenter(IGCDPresenter, ITaskPresenter[IGCDView]):
    def __init__(self) -> None:
        self.view: IGCDView | None = None
        self.strategies: dict[str, type[BaseGCDStrategy]] = {
            "Классический": GCDMod,
            "Бинарный": GCDBinary,
            "Расширенный": GCDBezout
        }

    def attach_view(self, view: IGCDView) -> None:
        self.view = view
        self.view.set_strategies(list(self.strategies.keys()))

    def on_activate(self) -> None:
        """Вызывается при активации Presenter'а (например, при выборе алгоритма)"""
        if not self.view:
            raise ValueError("View не установлен")

        # Передаем доступные стратегии во View
        self.view.set_strategies(list(self.strategies.keys()))

        # Очищаем поля ввода и результаты
        self._reset_inputs()
        self._clear_results()

    def _reset_inputs(self) -> None:
        """Сбрасывает поля ввода"""
        if self.view:
            ...
            # Предположим, что в IGCDView есть метод reset_inputs()
            ## self.view.reset_inputs()

    def _clear_results(self) -> None:
        """Очищает результаты и логи"""
        if self.view:
            self.view.display_result("")
            self.view.display_logs([])

    def on_calculate(self) -> None:
        a_str, b_str = self.view.get_inputs()
        strategy_name = self.view.get_selected_strategy()

        try:
            a: int = int(a_str)
            b: int = int(b_str)
        except ValueError:
            self.view.show_error("Введите целые числа для a и b")
            return

        strategy_class: type[BaseGCDStrategy] = self.strategies.get(strategy_name)

        if not strategy_class:
            self.view.show_error(f"Неизвестный алгоритм: {strategy_name}")
            return

        try:
            strategy_class: BaseGCDStrategy = strategy_class()
            context: AlgorithmStrategyContext = AlgorithmStrategyContext(a, b)
            context.set_strategy(strategy_class)
            result: ResultDTO = context.execute()

            # Обновление UI
            self.view.display_result(str(result))
            self.view.display_logs(list(strategy_class.get_logs()))

        except Exception as e:
            self.view.show_error(str(e))
