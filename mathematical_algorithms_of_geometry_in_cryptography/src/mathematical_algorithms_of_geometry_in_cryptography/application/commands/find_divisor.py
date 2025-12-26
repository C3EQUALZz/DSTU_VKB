import logging
from dataclasses import dataclass
from typing import Final, final

from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.entities.pollard_rho_test import (
    PollardRhoTest,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.services.pollard_rho_service import (
    PollardRhoService,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.function_expression import (
    FunctionExpression,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.initial_value import (
    InitialValue,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.number import (
    Number,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class FindDivisorCommand:
    """Команда для поиска нетривиального делителя методом Полларда."""

    number: int
    initial_value: int
    function_expression: str


@final
class FindDivisorCommandHandler:
    """Обработчик команды поиска делителя методом Полларда."""

    def __init__(self, pollard_rho_service: PollardRhoService) -> None:
        """
        Инициализировать обработчик сервисом метода Полларда.

        :param pollard_rho_service: сервис для выполнения алгоритма Полларда
        """
        self._pollard_rho_service: Final[PollardRhoService] = pollard_rho_service

    def __call__(
        self,
        command: FindDivisorCommand,
    ) -> PollardRhoTest:
        """
        Обработать команду поиска делителя.

        :param command: команда с параметрами алгоритма
        :return: результат выполнения алгоритма Полларда
        """
        logger.info(
            "Начинается поиск делителя методом Полларда. "
            "Число: %s, начальное значение: %s, функция: %s",
            command.number,
            command.initial_value,
            command.function_expression,
        )

        # Создаем value objects
        number = Number(value=command.number)
        initial_value = InitialValue(value=command.initial_value)
        function_expression = FunctionExpression(expression=command.function_expression)

        logger.info("Созданы value objects: number=%s, initial_value=%s, function=%s", number, initial_value, function_expression)

        # Выполняем алгоритм
        test: PollardRhoTest = self._pollard_rho_service.find_divisor(
            n=number,
            c=initial_value,
            function=function_expression,
        )

        logger.info("Алгоритм Полларда выполнен. ID теста: %s", test.id)
        logger.info("Количество выполненных шагов: %s", test.steps_count)

        # Логируем результаты каждого шага
        for step in test.steps:
            logger.info(
                "Шаг %s: a=%s, b=%s, d=%s",
                step.step_number,
                step.a,
                step.b,
                step.d,
            )

        # Логируем итоговый результат
        if test.is_complete:
            if test.divisor is not None:
                logger.info(
                    "Найден нетривиальный делитель: %s (за %s шагов)",
                    test.divisor,
                    test.steps_count,
                )
            else:
                logger.info(
                    "Делитель не найден (выполнено %s шагов)",
                    test.steps_count,
                )

        return test

