"""Service for working with Geffe generator."""

import logging
from collections.abc import Iterable, Sequence
from typing import Final

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService

logger: Final[logging.Logger] = logging.getLogger(__name__)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.entities.register import (
    Register,
)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.services.register_service import (
    RegisterService,
)
from theory_of_pseudorandom_generators.domain.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.entities.geffe_generator import (
    GeffeGenerator,
)
from theory_of_pseudorandom_generators.domain.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.ports.geffe_generator_id_generator import (
    GeffeGeneratorIDGenerator,
)


class GeffeGeneratorService(DomainService):
    """Service for creating and managing Geffe generators."""

    def __init__(self, id_generator: GeffeGeneratorIDGenerator) -> None:
        """Initialize service with ID generator.

        Args:
            id_generator: Generator for creating Geffe generator IDs
        """
        super().__init__()
        self._id_generator: Final[GeffeGeneratorIDGenerator] = id_generator

    def create(
        self,
        register1: Register,
        register2: Register,
        register3: Register,
    ) -> GeffeGenerator:
        """Create a new Geffe generator.

        Args:
            register1: First LFSR register
            register2: Second LFSR register
            register3: Third LFSR register

        Returns:
            New Geffe generator instance
        """
        return GeffeGenerator(
            id=self._id_generator(),
            register1=register1,
            register2=register2,
            register3=register3,
        )

    @staticmethod
    def get_register_sequences(
        generator: GeffeGenerator,
        register_service: RegisterService,
    ) -> tuple[list[int], list[int], list[int]]:
        """Generate sequences for each register using original shifts.

        Temporary registers are created with the original shift values,
        so each call to next() already advances by shift positions.
        No decimation is needed.
        """
        seq1: list[int] = []
        seq2: list[int] = []
        seq3: list[int] = []
        col1 = generator.register1.column_index
        col2 = generator.register2.column_index
        col3 = generator.register3.column_index
        for _, state1, state2, state3 in GeffeGeneratorService._iter_combined_states(
            generator, register_service
        ):
            seq1.append(state1[col1])
            seq2.append(state2[col2])
            seq3.append(state3[col3])

        return seq1, seq2, seq3

    @staticmethod
    def get_steps(
        generator: GeffeGenerator,
        register_service: RegisterService,
        steps_limit: int | None = None,
    ) -> list[str]:
        """Generate step-by-step output strings for combined states."""
        steps: list[str] = []
        col1 = generator.register1.column_index
        col2 = generator.register2.column_index
        col3 = generator.register3.column_index
        for step, state1, state2, state3 in GeffeGeneratorService._iter_combined_states(
            generator, register_service
        ):
            x1 = state1[col1]
            x2 = state2[col2]
            x3 = state3[col3]
            step_lines = [
                f"Шаг {step}:",
                (
                    f"  LFSR1: {''.join(str(b) for b in state1)} -> "
                    f"выбранный бит (столбец {col1 + 1}): {x1}"
                ),
                (
                    f"  LFSR2: {''.join(str(b) for b in state2)} -> "
                    f"выбранный бит (столбец {col2 + 1}): {x2}"
                ),
                (
                    f"  LFSR3: {''.join(str(b) for b in state3)} -> "
                    f"выбранный бит (столбец {col3 + 1}): {x3}"
                ),
                f"  f(x1,x2,x3) = {GeffeGeneratorService._geffe_bit(x1, x2, x3)}",
            ]
            steps.append("\n".join(step_lines))
            if steps_limit is not None and steps_limit > 0 and step + 1 >= steps_limit:
                break
        return steps

    @staticmethod
    def get_final_sequence(
        seq1: Sequence[int],
        seq2: Sequence[int],
        seq3: Sequence[int],
        length: int | None = None,
    ) -> list[int]:
        """Combine three sequences using Geffe formula.

        If length is provided, sequences are repeated to match that length.
        Otherwise, the minimum length is used.
        """
        if not seq1 or not seq2 or not seq3:
            return []
        if length is None:
            length = min(len(seq1), len(seq2), len(seq3))
        final_sequence: list[int] = []
        for i in range(length):
            x1 = seq1[i % len(seq1)]
            x2 = seq2[i % len(seq2)]
            x3 = seq3[i % len(seq3)]
            result = GeffeGeneratorService._geffe_bit(x1, x2, x3)
            final_sequence.append(result)
        return final_sequence

    @staticmethod
    def get_decimal_sequence_from_bits(
        bit_sequence: Sequence[int],
        number_count: int,
        bit_block_size: int = 16,
    ) -> str:
        """Convert bit sequence into decimal numbers using fixed-size blocks."""
        if number_count <= 0 or not bit_sequence:
            return ""
        required_bits = number_count * bit_block_size
        bits = [str(bit_sequence[i % len(bit_sequence)]) for i in range(required_bits)]
        sequence = "".join(bits)
        decimal_numbers = [
            str(int(sequence[i : i + bit_block_size], 2))
            for i in range(0, required_bits, bit_block_size)
        ]
        return "\t".join(decimal_numbers)

    @staticmethod
    def _geffe_bit(x1: int, x2: int, x3: int) -> int:
        """Calculate one Geffe output bit."""
        return (x1 & x2) ^ (x2 & x3) ^ x3

    @staticmethod
    def _iter_combined_states(
        generator: GeffeGenerator,
        register_service: RegisterService,
    ) -> Iterable[tuple[int, tuple[int, ...], tuple[int, ...], tuple[int, ...]]]:
        """Yield combined register states using original shifts until repetition."""
        temp_register1 = register_service.create(
            polynomial_coefficients=generator.register1.polynomial_coefficients,
            start_position=generator.register1.start_position,
            shift=generator.register1.shift,
            column_index=generator.register1.column_index,
        )
        temp_register2 = register_service.create(
            polynomial_coefficients=generator.register2.polynomial_coefficients,
            start_position=generator.register2.start_position,
            shift=generator.register2.shift,
            column_index=generator.register2.column_index,
        )
        temp_register3 = register_service.create(
            polynomial_coefficients=generator.register3.polynomial_coefficients,
            start_position=generator.register3.start_position,
            shift=generator.register3.shift,
            column_index=generator.register3.column_index,
        )

        seen_states: set[tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]] = set()

        temp_register1.clear()
        temp_register2.clear()
        temp_register3.clear()

        step = 0
        while True:
            state1 = tuple(temp_register1.next())
            state2 = tuple(temp_register2.next())
            state3 = tuple(temp_register3.next())
            combined_state = (state1, state2, state3)
            if combined_state in seen_states:
                break
            seen_states.add(combined_state)
            yield step, state1, state2, state3
            step += 1
    
    @staticmethod
    def get_states(
        generator: GeffeGenerator,
        separator: str = " -> ",
    ) -> Iterable[str]:
        """Generate state strings for all period states.

        Args:
            generator: Geffe generator to generate from
            separator: Separator between state and result

        Yields:
            Formatted state strings
        """
        generator.clear()
        for i in range(generator.period):
            arr = generator.next_array()
            x1, x2, x3 = arr[0], arr[1], arr[2]
            result = GeffeGeneratorService._geffe_bit(x1, x2, x3)
            state_str = "".join(str(v) for v in arr)
            yield f"{i}. {state_str}{separator}{result}"

