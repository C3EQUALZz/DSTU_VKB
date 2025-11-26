"""Command handler for Geffe generator."""

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import final

from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.entities.register import (
    Register,
)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.services.register_service import (
    RegisterService,
)
from theory_of_pseudorandom_generators.domain.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.entities.geffe_generator import (
    GeffeGenerator,
)
from theory_of_pseudorandom_generators.domain.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.services.geffe_generator_service import (
    GeffeGeneratorService,
)

logger: logging.Logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class GeffeyPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommand:
    """Command for generating Geffe sequence."""

    # Register 1 parameters
    register1_polynomial: Sequence[int]
    register1_start_state: Sequence[int]
    register1_shift: int
    register1_column_index: int = 0

    # Register 2 parameters
    register2_polynomial: Sequence[int]
    register2_start_state: Sequence[int]
    register2_shift: int
    register2_column_index: int = 0

    # Register 3 parameters
    register3_polynomial: Sequence[int]
    register3_start_state: Sequence[int]
    register3_shift: int
    register3_column_index: int = 0

    # Output parameters
    number_count: int = 200


@final
class GeffeyPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommandHandler:
    """Handler for Geffe generator command."""

    def __init__(
        self,
        register_service: RegisterService,
        geffe_generator_service: GeffeGeneratorService,
    ) -> None:
        """Initialize handler with services.

        Args:
            register_service: Service for creating registers
            geffe_generator_service: Service for creating Geffe generators
        """
        self._register_service: RegisterService = register_service
        self._geffe_generator_service: GeffeGeneratorService = geffe_generator_service

    def __call__(
        self,
        command: GeffeyPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommand,
    ) -> None:
        """Handle Geffe generator command.

        Args:
            command: Command with generator parameters
        """
        logger.info(
            "Начинается генерация псевдослучайных чисел с помощью генератора Геффе."
        )

        # Create registers
        register1: Register = self._register_service.create(
            polynomial_coefficients=command.register1_polynomial,
            start_position=command.register1_start_state,
            shift=command.register1_shift,
            column_index=command.register1_column_index,
        )

        register2: Register = self._register_service.create(
            polynomial_coefficients=command.register2_polynomial,
            start_position=command.register2_start_state,
            shift=command.register2_shift,
            column_index=command.register2_column_index,
        )

        register3: Register = self._register_service.create(
            polynomial_coefficients=command.register3_polynomial,
            start_position=command.register3_start_state,
            shift=command.register3_shift,
            column_index=command.register3_column_index,
        )

        logger.info("Создание регистров успешно!")

        # Create Geffe generator
        generator: GeffeGenerator = self._geffe_generator_service.create(
            register1=register1,
            register2=register2,
            register3=register3,
        )

        logger.info("Создание генератора Геффе успешно!")
        logger.info("%s", generator)

        # Generate and print states
        logger.info("Промежуточные результаты:")
        states = list(
            self._geffe_generator_service.get_states(generator, separator=" -> ")
        )
        states_output = "\n".join(states)
        logger.info(states_output)

        # Convert to decimal
        decimal_sequence = self._geffe_generator_service.get_decimal_sequence(
            generator, command.number_count
        )
        logger.info("Десятичные значения:")
        logger.info(decimal_sequence)

        # Save to file
        path_to_save: Path = Path(__file__).parent.parent.parent.parent.parent / "Geffey.txt"

        try:
            with open(path_to_save, "w", encoding="utf-8") as f:
                f.write(f"{generator}\n")
                f.write("\n".join(states) + "\n")
                f.write("Десятичные значения:\n")
                f.write(decimal_sequence)
            logger.info("Значения сохранены в файл: %s", path_to_save)
        except OSError as e:
            logger.error("Ошибка при сохранении файла: %s", e)


