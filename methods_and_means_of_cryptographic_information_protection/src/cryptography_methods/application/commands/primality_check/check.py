from dataclasses import dataclass
from typing import Final, final

from cryptography_methods.application.common.views.primality_check import (
    PrimalityCheckView,
)
from cryptography_methods.domain.zero_knowledge_proof.services.prime_number_service import (
    PrimeNumberService,
)


@dataclass(frozen=True, slots=True)
class PrimalityCheckCommand:
    number: int
    iterations: int = 20


@final
class PrimalityCheckCommandHandler:
    def __init__(
        self,
        prime_number_service: PrimeNumberService,
    ) -> None:
        self._prime_number_service: Final[PrimeNumberService] = (
            prime_number_service
        )

    async def __call__(
        self,
        data: PrimalityCheckCommand,
    ) -> PrimalityCheckView:
        is_prime: bool = self._prime_number_service.miller_rabin_test(
            n=data.number,
            k=data.iterations,
        )

        return PrimalityCheckView(
            number=data.number,
            is_prime=is_prime,
            iterations=data.iterations,
        )
