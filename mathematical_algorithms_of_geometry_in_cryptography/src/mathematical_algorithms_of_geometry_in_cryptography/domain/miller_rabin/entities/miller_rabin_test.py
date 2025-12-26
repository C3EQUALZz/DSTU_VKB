import logging
from dataclasses import dataclass, field
from typing import Final

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.entities.base_aggregate import (
    BaseAggregateRoot,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.errors.miller_rabin_errors import (
    CantAddResultError
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.values.miller_rabin_id import MillerRabinID
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.values.number import Number
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.values.test_result import (
    PrimalityStatus,
    TestResult,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(eq=False, kw_only=True)
class MillerRabinTest(BaseAggregateRoot[MillerRabinID]):
    """
    Aggregate root representing a Miller-Rabin primality test.
    
    This aggregate encapsulates:
    - The number being tested
    - All test iteration results
    - The overall test status
    
    The test is considered successful if all iterations pass (number is probably prime).
    """

    number: Number
    results: list[TestResult] = field(default_factory=list)
    is_complete: bool = field(default=False)

    def add_result(self, result: TestResult) -> None:
        """
        Add a test result to the aggregate.
        
        Args:
            result: The test result to add
            
        Raises:
            ValueError: If the test is already complete or result iteration is invalid
        """
        if self.is_complete:
            msg = "Не удается добавить результат к завершенному тесту"
            raise CantAddResultError(msg)

        if result.iteration != len(self.results) + 1:
            msg = (
                f"Ожидалась итерация {len(self.results) + 1}, "
                f"получил {result.iteration}"
            )
            raise CantAddResultError(msg)

        self.results.append(result)

        # If any iteration shows the number is composite, mark as complete
        if result.status == PrimalityStatus.COMPOSITE:
            self.is_complete = True

    def mark_complete(self) -> None:
        """Mark the test as complete (all iterations passed)."""
        self.is_complete = True

    @property
    def is_probably_prime(self) -> bool:
        """
        Check if the number is probably prime based on all test results.
        
        Returns:
            True if all iterations passed (probably prime), False otherwise
        """
        if not self.results:
            return False

        return all(
            result.status == PrimalityStatus.PROBABLY_PRIME
            for result in self.results
        )

    @property
    def is_composite(self) -> bool:
        """
        Check if the number is composite based on test results.
        
        Returns:
            True if any iteration shows the number is composite, False otherwise
        """
        return any(
            result.status == PrimalityStatus.COMPOSITE
            for result in self.results
        )

    @property
    def iterations_count(self) -> int:
        """Get the number of completed iterations."""
        return len(self.results)

