from app.application.analyzers.base import IAnalyzerComponent
from app.domain.calculators.dtos.halstead import HalsteadDTO
from app.infrastructure.persistence.base import IProcessor
from typing import override


class ConsoleProcessor(IProcessor):
    def __init__(
            self,
            dto: HalsteadDTO,
            analyzer: IAnalyzerComponent
    ) -> None:
        self._dto: HalsteadDTO = dto
        self._analyzer: IAnalyzerComponent = analyzer

    @override
    def process(self) -> None:
        results = (
            "\nРезультаты анализа:",
            f"Операторов: {self._analyzer.stats['operators_count']}",
            f"Операндов: {self._analyzer.stats['operands_count']}",
            f"Присваивания: {self._analyzer.stats['assignments']}",
            f"Ветвления: {self._analyzer.stats['branches']}",
            f"Циклы: {self._analyzer.stats['loops']}",
            f"Вызовы функций: {self._analyzer.stats['function_calls']}",
            f"Импорты: {self._analyzer.stats['imports']}",
            f"Обработка исключений: {self._analyzer.stats['exceptions']}"
        )

        print("\n".join(results))
