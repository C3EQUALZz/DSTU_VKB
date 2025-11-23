"""Register ID generator port."""

from abc import abstractmethod
from typing import Protocol

from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.values.register_id import (
    RegisterID,
)


class RegisterIDGenerator(Protocol):
    """Protocol for generating Register IDs."""

    @abstractmethod
    def __call__(self) -> RegisterID:
        """Generate a new Register ID."""
        ...

