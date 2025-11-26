"""Geffe generator ID generator port."""

from abc import abstractmethod
from typing import Protocol

from theory_of_pseudorandom_generators.domain.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.values.geffe_generator_id import (
    GeffeGeneratorID,
)


class GeffeGeneratorIDGenerator(Protocol):
    """Protocol for generating Geffe generator IDs."""

    @abstractmethod
    def __call__(self) -> GeffeGeneratorID:
        """Generate a new Geffe generator ID."""
        ...


