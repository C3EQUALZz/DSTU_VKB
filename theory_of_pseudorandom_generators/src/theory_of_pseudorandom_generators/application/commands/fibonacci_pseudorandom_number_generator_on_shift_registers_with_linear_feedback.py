"""Command handler for Fibonacci generator."""

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
    """Command for generating Fibonacci sequence."""

    polynomial_coefficients: Sequence[int]
    start_state: Sequence[int]
    shift: int
    column_index: int = 0


@final
class FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommandHandler:
    """Handler for Fibonacci generator command."""

    def __init__(self, register_service: RegisterService) -> None:
        """Initialize handler with register service.

        Args:
            register_service: Service for working with registers
        """
        self._register_service: Final[RegisterService] = register_service

    def __call__(
        self,
        command: FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommand,
    ) -> None:
        """Handle Fibonacci generator command.

        Args:
            command: Command with generator parameters
        """
        logger.info(
            "Начинается генерация псевдослучайных чисел с помощью генератора Фибоначчи. "
            "Полином: %s, Начальное состояние: %s, Сдвиг: %s, Индекс колонки: %s",
            command.polynomial_coefficients,
            command.start_state,
            command.shift,
            command.column_index,
        )

        # Create register
        register: Register = self._register_service.create(
            polynomial_coefficients=command.polynomial_coefficients,
            start_position=command.start_state,
            shift=command.shift,
            column_index=command.column_index,
        )

        logger.info("Создание регистра успешно!")
        logger.info("%s", register)

        # Generate sequence
        logger.info("Значения регистра:")
        binary_sequence = list(self._register_service.get_binary_sequence(register))
        
        # Add decimal representation of start state (last element in Java output)
        start_state_binary = "".join(str(bit) for bit in register.start_position)
        start_state_decimal = int(start_state_binary, 2) if start_state_binary else 0

        # Print intermediate results (matching Java output format)
        # Java: binary states -> ... -> decimal of start state
        output_separator = " -> "
        output = output_separator.join(binary_sequence) + output_separator + str(start_state_decimal)
        logger.info(output)

        # Calculate period
        period = register.get_period()
        max_period = register.max_period

        logger.info("Период генератора: %s", period)
        logger.info("S = 2^n - 1 = %s", max_period)
        is_max = period == max_period
        logger.info(
            "Период генератора %s максимальный.",
            "" if is_max else "не",
        )

        # Save sequence to file (without separators, matching Java format)
        file_path = Path.home() / "Desktop" / "Fibonacci.txt"
        file_output = "".join(binary_sequence) + str(start_state_decimal)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(file_output)
            logger.info("Значения сохранены в файл: %s", file_path)
        except OSError as e:
            logger.error("Ошибка при сохранении файла: %s", e)

