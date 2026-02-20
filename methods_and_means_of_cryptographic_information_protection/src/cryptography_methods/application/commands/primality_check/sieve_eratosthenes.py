from dataclasses import dataclass
from typing import Final, final

from cryptography_methods.application.common.views.sieve_eratosthenes import (
    SieveEratosthenesView,
    SieveRowView,
)
from cryptography_methods.domain.zero_knowledge_proof.services.prime_number_service import (
    PrimeNumberService,
)


@dataclass(frozen=True, slots=True)
class SieveEratosthenesCommand:
    start: int = 500
    end: int = 700
    max_k: int = 10


@final
class SieveEratosthenesCommandHandler:
    def __init__(
        self,
        prime_number_service: PrimeNumberService,
    ) -> None:
        self._prime: Final[PrimeNumberService] = (
            prime_number_service
        )

    async def __call__(
        self,
        data: SieveEratosthenesCommand,
    ) -> SieveEratosthenesView:
        total = data.end - data.start - 1
        rows: list[SieveRowView] = []

        for k in range(1, data.max_k + 1):
            primes_used = (
                PrimeNumberService._FIRST_PRIMES[:k]
            )
            passing = 0
            for n in range(data.start + 1, data.end):
                if self._prime.trial_division_test(
                    n, num_primes=k,
                ):
                    passing += 1

            relative = passing / total if total > 0 else 0.0
            rows.append(SieveRowView(
                k=k,
                primes_used=primes_used,
                passing_count=passing,
                total_count=total,
                relative_count=relative,
            ))

        return SieveEratosthenesView(
            interval_start=data.start,
            interval_end=data.end,
            rows=tuple(rows),
        )
