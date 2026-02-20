from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PrimeResultPerMethod:
    number: int
    trial_division: bool
    fermat: bool
    miller_rabin: bool


@dataclass(frozen=True, slots=True)
class FindPrimesInIntervalView:
    interval_start: int
    interval_end: int
    num_trial_primes: int
    num_fermat_bases: int
    miller_rabin_iterations: int
    results_per_number: tuple[PrimeResultPerMethod, ...]
    primes: tuple[int, ...]
    gaps: tuple[int, ...]
    mean_gap: float
    ln_mid: float
    histogram: dict[int, int]
