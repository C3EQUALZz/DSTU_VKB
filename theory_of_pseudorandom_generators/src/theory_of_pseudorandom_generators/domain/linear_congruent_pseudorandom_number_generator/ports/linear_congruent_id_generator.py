from abc import abstractmethod
from typing import Protocol

from theory_of_pseudorandom_generators.domain.linear_congruent_pseudorandom_number_generator.values.linear_congruent_generator_id import (
    LinearCongruentGeneratorID
)


class LinearCongruentIDGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> LinearCongruentGeneratorID:
        ...
