from dataclasses import dataclass
from math import gcd
from typing import Final, final

from cryptography_methods.application.common.views.carmichael import (
    CarmichaelNumberView,
    FindCarmichaelView,
)
from cryptography_methods.domain.zero_knowledge_proof.services.prime_number_service import (
    PrimeNumberService,
)


@dataclass(frozen=True, slots=True)
class FindCarmichaelCommand:
    start: int = 1
    end: int = 10000


def _factorize(n: int) -> list[int]:
    factors: list[int] = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def _is_carmichael(n: int) -> tuple[bool, tuple[int, ...]]:
    if n < 2:  # noqa: PLR2004
        return False, ()

    factors = _factorize(n)

    if len(factors) < 2:  # noqa: PLR2004
        return False, ()

    unique = set(factors)
    if len(factors) != len(unique):
        return False, ()

    for p in unique:
        if (n - 1) % (p - 1) != 0:
            return False, ()

    return True, tuple(sorted(unique))


@final
class FindCarmichaelCommandHandler:
    def __init__(
        self,
        prime_number_service: PrimeNumberService,
    ) -> None:
        self._prime: Final[PrimeNumberService] = (
            prime_number_service
        )

    async def __call__(
        self,
        data: FindCarmichaelCommand,
    ) -> FindCarmichaelView:
        results: list[CarmichaelNumberView] = []
        total = 0

        for n in range(data.start + 1, data.end):
            total += 1
            is_carm, factors = _is_carmichael(n)
            if not is_carm:
                continue

            passes = self._prime.fermat_test(n, num_bases=5)
            results.append(CarmichaelNumberView(
                number=n,
                prime_factors=factors,
                passes_fermat=passes,
            ))

        return FindCarmichaelView(
            interval_start=data.start,
            interval_end=data.end,
            carmichael_numbers=tuple(results),
            total_checked=total,
        )
