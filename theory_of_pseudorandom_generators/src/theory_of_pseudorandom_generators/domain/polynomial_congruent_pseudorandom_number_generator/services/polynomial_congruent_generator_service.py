"""Service for working with polynomial congruent generator."""

from collections import deque
from collections.abc import Iterable
from typing import Final

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService
from theory_of_pseudorandom_generators.domain.polynomial_congruent_pseudorandom_number_generator.entities.polynomial_congruent_generator import (
    PolynomialCongruentGenerator,
)
from theory_of_pseudorandom_generators.domain.polynomial_congruent_pseudorandom_number_generator.ports.polynomial_congruent_id_generator import (
    PolynomialCongruentIDGenerator,
)


class PolynomialCongruentGeneratorService(DomainService):
    """Service for creating and managing polynomial congruent generators."""

    def __init__(self, id_generator: PolynomialCongruentIDGenerator) -> None:
        """Initialize service with ID generator.

        Args:
            id_generator: Generator for creating polynomial congruent generator IDs
        """
        super().__init__()
        self._id_generator: Final[PolynomialCongruentIDGenerator] = id_generator

    def create(
        self,
        a1: int,
        a2: int,
        b: int,
        x: int,
        m: int,
    ) -> PolynomialCongruentGenerator:
        """Create a new polynomial congruent generator.

        Args:
            a1: Coefficient a1
            a2: Coefficient a2
            b: Coefficient b
            x: Initial value x0
            m: Modulus

        Returns:
            New polynomial congruent generator instance
        """
        return PolynomialCongruentGenerator(
            id=self._id_generator(),
            a1=a1,
            a2=a2,
            b=b,
            x=x,
            m=m,
        )

    @staticmethod
    def get_random_sequence(
        generator: PolynomialCongruentGenerator,
        count: int,
    ) -> Iterable[int]:
        """Generate a sequence of pseudorandom numbers.

        Args:
            generator: The generator entity
            count: Number of elements to generate

        Returns:
            Sequence of generated numbers
        """
        sequence: deque[int] = deque([generator.x])
        current: int = generator.x

        for _ in range(1, count):
            current = generator.next(current)
            sequence.append(current)

        return sequence

    @staticmethod
    def is_maximized_period(
        generator: PolynomialCongruentGenerator,
    ) -> bool:
        """Check if the generator has maximum period (m).

        Note: This is a simplified check. Full conditions for maximum period
        in quadratic congruent generators are more complex than linear ones.

        Args:
            generator: The generator entity

        Returns:
            True if period might be maximized, False otherwise
        """
        # Basic check: if all parameters are valid and generator works
        # Full maximum period conditions for quadratic generators are complex
        # and depend on prime factorization of m
        # For now, we'll do a basic validation
        if generator.m <= 1:
            return False

        # Check if parameters are in valid range
        if not (0 <= generator.a1 < generator.m):
            return False
        if not (0 <= generator.a2 < generator.m):
            return False
        if not (0 <= generator.b < generator.m):
            return False
        if not (0 <= generator.x < generator.m):
            return False

        # More detailed checks would require analysis of m's prime factors
        # For now, return True if basic conditions are met
        # Actual period calculation will be done by get_period()
        return True

    @staticmethod
    def get_period(
        generator: PolynomialCongruentGenerator,
    ) -> int:
        """Get the period of the sequence using Floyd's cycle detection.

        Args:
            generator: The generator entity

        Returns:
            The period length
        """
        # Floyd's cycle detection algorithm
        turtle = generator.next(generator.x)
        hare = generator.next(generator.next(generator.x))

        # Find meeting point
        while turtle != hare:
            turtle = generator.next(turtle)
            hare = generator.next(generator.next(hare))

        # Find start of cycle
        turtle = generator.x
        while turtle != hare:
            turtle = generator.next(turtle)
            hare = generator.next(hare)

        # Measure period length
        hare = generator.next(turtle)
        period = 1
        while turtle != hare:
            hare = generator.next(hare)
            period += 1

        return period

    @staticmethod
    def get_start_period_index(
        generator: PolynomialCongruentGenerator,
    ) -> int:
        """Get the index where the period starts.

        Args:
            generator: The generator entity

        Returns:
            Index of period start
        """
        # Floyd's cycle detection algorithm
        turtle = generator.next(generator.x)
        hare = generator.next(generator.next(generator.x))

        # Find meeting point
        while turtle != hare:
            turtle = generator.next(turtle)
            hare = generator.next(generator.next(hare))

        # Find start of cycle
        turtle = generator.x
        start = 0
        while turtle != hare:
            turtle = generator.next(turtle)
            hare = generator.next(hare)
            start += 1

        return start


