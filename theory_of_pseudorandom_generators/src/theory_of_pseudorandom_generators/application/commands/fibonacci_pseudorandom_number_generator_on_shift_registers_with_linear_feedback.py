"""Командный обработчик для генератора Фибоначчи."""

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.entities.register import (
    Register,
)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.services.register_service import (
    RegisterService,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommand:
    """Команда для генерации последовательности Фибоначчи."""

    polynomial_coefficients: Sequence[int]
    start_state: Sequence[int]
    shift: int
    column_index: int = 0


@final
class FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommandHandler:
    """Обработчик команды генератора Фибоначчи."""

    def __init__(self, register_service: RegisterService) -> None:
        """
        Инициализировать обработчик сервисом работы с регистрами.

        :param register_service: сервис для работы с регистрами
        """
        self._register_service: Final[RegisterService] = register_service

    def __call__(
        self,
        command: FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommand,
    ) -> None:
        """
        Обработать команду генератора Фибоначчи.

        :param command: команда с параметрами генератора
        """
        logger.info(
            "Начинается генерация псевдослучайных чисел с помощью генератора Фибоначчи. "
            "Полином: %s, Начальное состояние: %s, Сдвиг: %s, Индекс колонки: %s",
            command.polynomial_coefficients,
            command.start_state,
            command.shift,
            command.column_index,
        )

        # Создаем регистр
        register: Register = self._register_service.create(
            polynomial_coefficients=command.polynomial_coefficients,
            start_position=command.start_state,
            shift=command.shift,
            column_index=command.column_index,
        )

        logger.info("Создание регистра успешно!")
        logger.info("%s", register)

        # Генерируем последовательность
        binary_sequence = list(self._register_service.get_binary_sequence(register))

        # Добавляем десятичное представление начального состояния
        start_state_binary = "".join(str(bit) for bit in register.start_position)
        start_state_decimal = int(start_state_binary, 2) if start_state_binary else 0

        # Формируем строку промежуточных результатов
        output_separator = " -> "
        output = output_separator.join(binary_sequence) + output_separator + str(start_state_decimal)
        logger.info("Значения регистра: %s", output)

        # Генерируем десятичную последовательность для сохранения в файл
        decimal_sequence = list(self._register_service.get_decimal_sequence(register))
        
        # Формируем строку десятичных значений с табуляцией
        decimal_values_str = "\t".join(str(num) for num in decimal_sequence)
        logger.info("Десятичные значения: %s", decimal_values_str[:200] + ("..." if len(decimal_values_str) > 200 else ""))

        # Вычисляем период
        period = register.get_period()
        max_period = register.max_period

        logger.info("Период генератора: %s", period)
        logger.info("S = 2^n - 1 = %s", max_period)
        is_max = period == max_period
        logger.info(
            "Период генератора %s максимальный.",
            "" if is_max else "не",
        )

        path_to_save: Path = Path(__file__).parent.parent.parent.parent.parent / "Fibonacci.txt"

        try:
            with open(path_to_save, "w", encoding="utf-8") as f:
                f.write(decimal_values_str)
            logger.info("Значения сохранены в файл: %s", path_to_save)
        except OSError as e:
            logger.error("Ошибка при сохранении файла: %s", e)



