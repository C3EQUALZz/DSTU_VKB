from math import gcd
from typing import Final, List, Iterable
from collections import deque

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService
from theory_of_pseudorandom_generators.domain.linear_congruent_pseudorandom_number_generator.entities.linear_congruent_generator import (
    LinearCongruentGenerator,
)
from theory_of_pseudorandom_generators.domain.linear_congruent_pseudorandom_number_generator.ports.linear_congruent_id_generator import (
    LinearCongruentIDGenerator,
)


class LinearCongruentGeneratorService(DomainService):
    def __init__(self, id_generator: LinearCongruentIDGenerator) -> None:
        super().__init__()
        self._id_generator: Final[LinearCongruentIDGenerator] = id_generator

    def create(
        self,
        a: int,
        b: int,
        x: int,
        m: int,
    ) -> LinearCongruentGenerator:
        """Create a new linear congruent generator."""
        new_entity = LinearCongruentGenerator(
            id=self._id_generator(),
            a=a,
            b=b,
            x=x,
            m=m,
        )

        return new_entity

    # noinspection PyMethodMayBeStatic
    def get_random_sequence(
        self,
        generator: LinearCongruentGenerator,
        count: int,
    ) -> Iterable[int]:
        """
        Generate a sequence of pseudorandom numbers.

        Args:
            generator: The generator entity
            count: Number of elements to generate

        Returns:
            List of generated numbers
        """
        sequence: deque[int] = deque([generator.x])
        current: int = generator.x

        for _ in range(1, count):
            current: int = generator.next(current)
            sequence.append(current)

        return sequence

    # noinspection PyMethodMayBeStatic
    def is_maximized_period(
        self,
        generator: LinearCongruentGenerator,
    ) -> bool:
        """
        Check if the generator has maximum period (m).

        Args:
            generator: The generator entity

        Returns:
            True if period is maximized, False otherwise
        """
        # Check if gcd(b, m) == 1
        if gcd(generator.b, generator.m) != 1:
            return False

        # Get multipliers of m (includes 1)
        multipliers = self.__get_multipliers_list(generator.m)

        # Check if (a - 1) is divisible by all multipliers
        if any((generator.a - 1) % x != 0 for x in multipliers):
            return False

        # Check if m is divisible by 4
        if generator.m % 4 != 0:
            return False

        # Check if all multipliers satisfy (x - 1) % 4 == 0
        return all((x - 1) % 4 == 0 for x in multipliers)

    def get_period(
        self,
        generator: LinearCongruentGenerator,
    ) -> int:
        """
        Get the period of the sequence using Floyd's cycle detection.

        Args:
            generator: The generator entity

        Returns:
            The period length
        """
        if self.is_maximized_period(generator):
            return generator.m

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

    # noinspection PyMethodMayBeStatic
    def get_start_period_index(
        self,
        generator: LinearCongruentGenerator,
    ) -> int:
        """
        Get the index where the period starts.

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

    @staticmethod
    def __get_multipliers_list(number: int) -> List[int]:
        """
            Get list of prime multipliers for a given number.

            Args:
                number: The number to factorize

            Returns:
                List of prime multipliers (including 1)

            Example:
                get_multipliers_list(12) -> [1, 2, 2, 3]
            """
        if number == 0:
            return [0]

        multipliers: List[int] = [1]
        divider = 2

        while number != 1:
            if number % divider != 0:
                divider += 1
                continue
            number //= divider
            multipliers.append(divider)

        return multipliers


