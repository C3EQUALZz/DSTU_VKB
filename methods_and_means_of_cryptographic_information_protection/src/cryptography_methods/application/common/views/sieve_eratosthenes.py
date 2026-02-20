from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SieveRowView:
    k: int
    primes_used: tuple[int, ...]
    passing_count: int
    total_count: int
    relative_count: float


@dataclass(frozen=True, slots=True)
class SieveEratosthenesView:
    interval_start: int
    interval_end: int
    rows: tuple[SieveRowView, ...]
