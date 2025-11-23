"""Service for working with Geffe generator."""

from collections.abc import Iterable
from typing import Final

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.entities.register import (
    Register,
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
            # Calculate result using Geffe formula
            x1, x2, x3 = arr[0], arr[1], arr[2]
            result = ((x1 & x2) + (x2 & x3)) % 2
            result = (result + x3) % 2
            state_str = "".join(str(v) for v in arr)
            yield f"{i}. {state_str}{separator}{result}"

    @staticmethod
    def get_decimal_sequence(
        generator: GeffeGenerator,
        number_count: int,
    ) -> str:
        """Convert binary sequence to decimal numbers.

        Args:
            generator: Geffe generator to generate from
            number_count: Number of decimal numbers to generate

        Returns:
            Tab-separated decimal sequence
        """
        sequence = generator.get_sequence()
        max_bit_count = len(sequence) // number_count if number_count > 0 else len(sequence)

        decimal_numbers = []
        for i in range(number_count):
            start_index = i * max_bit_count
            end_index = min(start_index + max_bit_count, len(sequence))
            if start_index < len(sequence):
                binary_str = sequence[start_index:end_index]
                decimal_num = int(binary_str, 2) if binary_str else 0
                decimal_numbers.append(str(decimal_num))

        return "\t".join(decimal_numbers)

