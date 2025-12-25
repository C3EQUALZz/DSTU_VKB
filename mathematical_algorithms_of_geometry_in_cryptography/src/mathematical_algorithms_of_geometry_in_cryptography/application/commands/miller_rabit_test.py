import logging
from dataclasses import dataclass
from typing import Final, Optional, final

from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.entities.miller_rabin_test import (
    MillerRabinTest,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.services.miller_rabin_service import (
    MillerRabinService,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.values.number import (
    Number,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class MakeMillerRabinTestCommand:
    """Команда для выполнения теста Миллера-Рабина."""

    number: int
    iterations: int = 5
    random_seed: Optional[int] = None


@final
class MakeMillerRabitTestCommandHandler:
    """Обработчик команды теста Миллера-Рабина."""

    def __init__(self, miller_rabin_service: MillerRabinService) -> None:
        """
        Инициализировать обработчик сервисом теста Миллера-Рабина.

        :param miller_rabin_service: сервис для выполнения теста Миллера-Рабина
        """
        self._miller_rabin_service: Final[MillerRabinService] = miller_rabin_service

    def __call__(
        self,
        command: MakeMillerRabinTestCommand,
    ) -> MillerRabinTest:
        """
        Обработать команду теста Миллера-Рабина.

        :param command: команда с параметрами теста
        :return: результат теста Миллера-Рабина
        """
        logger.info(
            "Начинается тест Миллера-Рабина для числа: %s. "
            "Количество итераций: %s. Random seed: %s",
            command.number,
            command.iterations,
            command.random_seed,
        )

        # Создаем Number value object
        number = Number(value=command.number)
        logger.info("Создан объект Number: %s", number)

        # Выполняем полный тест
        test: MillerRabinTest = self._miller_rabin_service.perform_full_test(
            n=number,
            iterations=command.iterations,
            random_seed=command.random_seed,
        )

        logger.info("Тест Миллера-Рабина выполнен. ID теста: %s", test.id)
        logger.info("Количество выполненных итераций: %s", test.iterations_count)

        # Логируем результаты каждой итерации
        for result in test.results:
            logger.info(
                "Итерация %s: статус = %s, параметры (s=%s, t=%s, a=%s)",
                result.iteration,
                result.status.value,
                result.parameters.s,
                result.parameters.t,
                result.parameters.a,
            )

            # Логируем промежуточные значения
            for key, value in result.intermediate_values.items():
                logger.info("  %s = %s", key, value)

        # Логируем итоговый результат
        if test.is_complete:
            if test.is_probably_prime:
                logger.info(
                    "Тест завершен. Число %s вероятно простое (все %s итераций пройдены)",
                    command.number,
                    test.iterations_count,
                )
            elif test.is_composite:
                logger.info(
                    "Тест завершен. Число %s составное (обнаружено на итерации %s)",
                    command.number,
                    test.iterations_count,
                )
        else:
            logger.warning(
                "Тест не завершен. Выполнено %s из %s итераций",
                test.iterations_count,
                command.iterations,
            )

        return test
