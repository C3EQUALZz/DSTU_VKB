from typing import Dict, Type

from app.core.dto import ResultDTO
from app.core.interfaces.presenter import GCDPresenterInterface
from app.core.interfaces.view import GCDViewInterface
from app.models.base import BaseGCDStrategy
from app.presenters.context import AlgorithmStrategyContext


class GCDCalculatorPresenter(GCDPresenterInterface):
    def __init__(
            self,
            view: GCDViewInterface,
            strategies: Dict[str, Type[BaseGCDStrategy]],
    ) -> None:
        self.view: GCDViewInterface = view
        self.strategies: Dict[str, Type[BaseGCDStrategy]] = strategies
        self.view.set_strategies(list(strategies.keys()))

    def on_calculate(self) -> None:
        a_str, b_str = self.view.get_inputs()
        strategy_name = self.view.get_selected_strategy()

        try:
            a: int = int(a_str)
            b: int = int(b_str)
        except ValueError:
            self.view.show_error("Введите целые числа для a и b")
            return

        strategy_class: Type[BaseGCDStrategy] = self.strategies.get(strategy_name)

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
