"""Polynomial congruent ID generator port."""

from abc import abstractmethod
from typing import Protocol

from theory_of_pseudorandom_generators.domain.polynomial_congruent_pseudorandom_number_generator.values.polynomial_congruent_generator_id import (
    PolynomialCongruentGeneratorID,
)


class PolynomialCongruentIDGenerator(Protocol):
    """Protocol for generating Polynomial Congruent IDs."""

    @abstractmethod
    def __call__(self) -> PolynomialCongruentGeneratorID:
        """Generate a new Polynomial Congruent Generator ID."""
        ...




