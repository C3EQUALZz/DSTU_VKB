"""Command handler for Geffe generator."""

import logging
from pathlib import Path
from collections.abc import Sequence
from dataclasses import dataclass
from typing import final

from theory_of_pseudorandom_generators.application.views.geffe_generator_view import (
    GeffeGeneratorView,
)
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
    show_steps: bool = False
    steps_limit: int = 0


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
    ) -> GeffeGeneratorView:
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

        # Get periods
        max_period1 = register1.max_period
        max_period2 = register2.max_period
        max_period3 = register3.max_period
        theoretical_period = generator.period
        
        # Calculate actual sequence period (L)
        actual_period = generator.get_actual_sequence_period()
        
        # Generate decimated sequences for each register
        # Передаем register_service для создания временных регистров с shift=1
        seq1, seq2, seq3 = self._geffe_generator_service.get_register_sequences(
            generator, self._register_service
        )
        
        # Generate final sequence using Geffe function in service
        final_sequence = self._geffe_generator_service.get_final_sequence(seq1, seq2, seq3)
        logger.info(
            "Длины последовательностей: seq1=%s, seq2=%s, seq3=%s, min_len=%s",
            len(seq1),
            len(seq2),
            len(seq3),
            len(final_sequence),
        )
        
        # Convert final sequence to decimal (whole number)
        final_binary_str = "".join(str(b) for b in final_sequence)
        logger.info("Длина итоговой двоичной последовательности: %s", len(final_binary_str))
        final_decimal = self._geffe_generator_service.binary_to_decimal_str(final_sequence)

        # Generate decimal numbers sequence from the final sequence
        decimal_sequence = self._geffe_generator_service.get_decimal_sequence_from_bits(
            final_sequence,
            command.number_count,
        )

        steps: tuple[str, ...] = ()
        if command.show_steps:
            steps_limit = None if command.steps_limit <= 0 else command.steps_limit
            steps = tuple(
                self._geffe_generator_service.get_steps(
                    generator,
                    self._register_service,
                    steps_limit,
                )
            )

        path_to_save: Path = (
            Path(__file__).parent.parent.parent.parent.parent / "Geffe.txt"
        )
        try:
            with open(path_to_save, "w", encoding="utf-8") as f:
                f.write(decimal_sequence)
            logger.info("Значения сохранены в файл: %s", path_to_save)
        except OSError as e:
            logger.error("Ошибка при сохранении файла: %s", e)
        
        # Create and return View
        return GeffeGeneratorView(
            register1_polynomial=tuple(command.register1_polynomial),
            register1_start_state=tuple(command.register1_start_state),
            register1_shift=command.register1_shift,
            register1_column_index=command.register1_column_index,
            register1_max_period=max_period1,
            register2_polynomial=tuple(command.register2_polynomial),
            register2_start_state=tuple(command.register2_start_state),
            register2_shift=command.register2_shift,
            register2_column_index=command.register2_column_index,
            register2_max_period=max_period2,
            register3_polynomial=tuple(command.register3_polynomial),
            register3_start_state=tuple(command.register3_start_state),
            register3_shift=command.register3_shift,
            register3_column_index=command.register3_column_index,
            register3_max_period=max_period3,
            theoretical_period=theoretical_period,
            actual_sequence_period=actual_period,
            register1_sequence=tuple(seq1),
            register2_sequence=tuple(seq2),
            register3_sequence=tuple(seq3),
            final_sequence=tuple(final_sequence),
            final_decimal=final_decimal,
            decimal_sequence=decimal_sequence,
            steps=steps,
        )


