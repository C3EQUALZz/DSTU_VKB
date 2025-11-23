"""Service for working with Fibonacci register."""

from collections.abc import Iterable, Sequence
from typing import Final

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.entities.register import (
    Register,
)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.ports.register_id_generator import (
    RegisterIDGenerator,
)


class RegisterService(DomainService):
    """Service for creating and managing Fibonacci registers."""

    def __init__(self, id_generator: RegisterIDGenerator) -> None:
        """Initialize service with ID generator.

        Args:
            id_generator: Generator for creating register IDs
        """
        super().__init__()
        self._id_generator: Final[RegisterIDGenerator] = id_generator

    def create(
        self,
        polynomial_coefficients: Sequence[int],
        start_position: Sequence[int],
        shift: int,
        column_index: int = 0,
    ) -> Register:
        """Create a new register.

        Args:
            polynomial_coefficients: Coefficients of primitive polynomial
            start_position: Initial register state
            shift: Shift value k
            column_index: Column index for output

        Returns:
            New register instance
        """
        return Register(
            id=self._id_generator(),
            polynomial_coefficients=polynomial_coefficients,
            start_position=start_position,
            shift=shift,
            column_index=column_index,
        )

    @staticmethod
    def get_sequence(register: Register, count: int | None = None) -> Iterable[Sequence[int]]:
        """Generate sequence of register states.

        Args:
            register: Register to generate from
            count: Number of states to generate (None for full period)

        Yields:
            Register states
        """
        register.clear()
        if count is None:
            # Generate full period (matching Java logic)
            # Start with first next() (not initial state)
            start_state = list(register.start_position)
            current = register.next()
            yield current
            current = register.next()
            while list(register._register[0]) != start_state:
                yield current
                current = register.next()
            # Last state (which equals start_state) is not yielded here
            # It will be converted to decimal in get_decimal_sequence
        else:
            for _ in range(count):
                yield register.next()

    @staticmethod
    def get_binary_sequence(register: Register, count: int | None = None) -> Iterable[str]:
        """Generate binary sequence from register.

        Args:
            register: Register to generate from
            count: Number of states to generate

        Yields:
            Binary strings representing register states
        """
        for state in RegisterService.get_sequence(register, count):
            yield "".join(str(bit) for bit in state)

    @staticmethod
    def get_decimal_sequence(register: Register, count: int | None = None) -> Iterable[int]:
        """Generate decimal sequence from binary register states.

        Args:
            register: Register to generate from
            count: Number of states to generate

        Yields:
            Decimal numbers converted from binary states
        """
        for binary_str in RegisterService.get_binary_sequence(register, count):
            yield int(binary_str, 2)

    @staticmethod
    def is_maximized_period(register: Register) -> bool:
        """Check if register has maximum period.

        Args:
            register: Register to check

        Returns:
            True if period is maximized (2^n - 1), False otherwise
        """
        period = register.get_period()
        return period == register.max_period

