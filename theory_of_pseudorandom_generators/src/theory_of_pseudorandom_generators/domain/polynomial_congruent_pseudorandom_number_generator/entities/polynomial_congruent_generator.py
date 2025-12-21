"""Polynomial congruent generator entity."""

from dataclasses import dataclass

from theory_of_pseudorandom_generators.domain.common.entities.base_aggregate import (
    BaseAggregateRoot,
)
from theory_of_pseudorandom_generators.domain.polynomial_congruent_pseudorandom_number_generator.errors import (
    WrongParameterValueError,
)
from theory_of_pseudorandom_generators.domain.polynomial_congruent_pseudorandom_number_generator.values.polynomial_congruent_generator_id import (
    PolynomialCongruentGeneratorID,
)


@dataclass(eq=False, kw_only=True)
class PolynomialCongruentGenerator(BaseAggregateRoot[PolynomialCongruentGeneratorID]):
    """Polynomial congruent generator: x_{n+1} = (a_2*x_n^2 + a_1*x_n + b) (mod m)."""

    a1: int
    a2: int
    b: int
    x: int
    m: int

    def __post_init__(self) -> None:
        """Validate generator parameters."""
        super().__post_init__()

        if self.m <= 0:
            msg = "Значение модуля должно быть больше нуля"
            raise WrongParameterValueError(msg)

        if self.a1 < 0 or self.a1 > self.m:
            msg = "Значение a1 должно находиться на отрезке [0, m]"
            raise WrongParameterValueError(msg)

        if self.a2 < 0 or self.a2 > self.m:
            msg = "Значение a2 должно находиться на отрезке [0, m]"
            raise WrongParameterValueError(msg)

        if self.b < 0 or self.b > self.m:
            msg = "Значение b должно находиться на отрезке [0, m]"
            raise WrongParameterValueError(msg)

        if self.x < 0 or self.x > self.m:
            msg = "Значение x0 должно находиться на отрезке [0, m]"
            raise WrongParameterValueError(msg)

    def next(self, seed: int) -> int:
        """Generate next number from seed.

        Formula: x_{n+1} = (a_2*x_n^2 + a_1*x_n + b) (mod m)

        Args:
            seed: Current value

        Returns:
            Next generated number
        """
        return (self.a2 * seed * seed + self.a1 * seed + self.b) % self.m

    def __str__(self) -> str:
        """String representation of the generator."""
        lines: list[str] = [
            f"a1 = {self.a1}",
            f"a2 = {self.a2}",
            f"b = {self.b}",
            f"X0 = {self.x}",
            f"m = {self.m}",
            "Общий вид:",
            (
                f"xₙ₊₁≡"
                f"{self.a2}*xₙ² + {self.a1}*xₙ + {self.b}"
                f"(mod {self.m})"
            ),
        ]
        return "\n".join(lines)




