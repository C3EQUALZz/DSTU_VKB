from dataclasses import dataclass

from theory_of_pseudorandom_generators.domain.common.entities.base_aggregate import BaseAggregateRoot
from theory_of_pseudorandom_generators.domain.linear_congruent_pseudorandom_number_generator.errors import (
    WrongParameterValueError,
)
from theory_of_pseudorandom_generators.domain.linear_congruent_pseudorandom_number_generator.values.linear_congruent_generator_id import (
    LinearCongruentGeneratorID,
)


@dataclass(eq=False, kw_only=True)
class LinearCongruentGenerator(BaseAggregateRoot[LinearCongruentGeneratorID]):
    a: int
    b: int
    x: int
    m: int

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.m <= 0:
            msg = "Значение модуля должно быть больше нуля"
            raise WrongParameterValueError(msg)

        if self.a < 0 or self.a > self.m:
            msg = "Значение a должно находиться на отрезке [0, m]"
            raise WrongParameterValueError(msg)

        if self.b < 0 or self.b > self.m:
            msg = "Значение b должно находиться на отрезке [0, m]"
            raise WrongParameterValueError(msg)

        if self.x < 0 or self.x > self.m:
            msg = "Значение x0 должно находиться на отрезке [0, m]"
            raise WrongParameterValueError(msg)

    def next(self, seed: int) -> int:
        """
        Generate next number from seed.

        Args:
            seed: Current value

        Returns:
            Next generated number
        """
        return (self.a * seed + self.b) % self.m

    def __str__(self) -> str:
        """String representation of the generator."""

        lines: list[str] = [
            f"a = {self.a}",
            f"b = {self.b}",
            f"X0 = {self.x}",
            f"m = {self.m}",
            "Общий вид:",
            (
                f"xₙ₊₁≡"
                f"{self.a}*xₙ + {self.b}"
                f"(mod {self.m})"
            ),
        ]

        return " ".join(lines)
