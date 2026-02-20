import math
from collections import Counter
from dataclasses import dataclass
from typing import Final, final

from cryptography_methods.application.common.views.find_primes_in_interval import (
    FindPrimesInIntervalView,
    PrimeResultPerMethod,
)
from cryptography_methods.domain.zero_knowledge_proof.services.prime_number_service import (
    PrimeNumberService,
)


@dataclass(frozen=True, slots=True)
class FindPrimesInIntervalCommand:
    start: int
    end: int
    num_trial_primes: int = 10
    num_fermat_bases: int = 2
    miller_rabin_iterations: int = 20


@final
class FindPrimesInIntervalCommandHandler:
    def __init__(
        self,
        prime_number_service: PrimeNumberService,
    ) -> None:
        self._prime: Final[PrimeNumberService] = (
            prime_number_service
        )

    async def __call__(
        self,
        data: FindPrimesInIntervalCommand,
    ) -> FindPrimesInIntervalView:
        results: list[PrimeResultPerMethod] = []

        for n in range(data.start + 1, data.end):
            td = self._prime.trial_division_test(
                n, data.num_trial_primes,
            )
            fm = self._prime.fermat_test(
                n, data.num_fermat_bases,
            )
            mr = self._prime.miller_rabin_test(
                n, data.miller_rabin_iterations,
            )
            if td or fm or mr:
                results.append(PrimeResultPerMethod(
                    number=n,
                    trial_division=td,
                    fermat=fm,
                    miller_rabin=mr,
                ))

        primes = tuple(
            r.number for r in results if r.miller_rabin
        )

        gaps = tuple(
            primes[i + 1] - primes[i]
            for i in range(len(primes) - 1)
        )

        mean_gap = (
            sum(gaps) / len(gaps) if gaps else 0.0
        )

        mid = (data.start + data.end) / 2.0
        ln_mid = math.log(mid)

        histogram = dict(sorted(Counter(gaps).items()))

        return FindPrimesInIntervalView(
            interval_start=data.start,
            interval_end=data.end,
            num_trial_primes=data.num_trial_primes,
            num_fermat_bases=data.num_fermat_bases,
            miller_rabin_iterations=data.miller_rabin_iterations,
            results_per_number=tuple(results),
            primes=primes,
            gaps=gaps,
            mean_gap=mean_gap,
            ln_mid=ln_mid,
            histogram=histogram,
        )
