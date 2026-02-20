from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CarmichaelNumberView:
    number: int
    prime_factors: tuple[int, ...]
    passes_fermat: bool


@dataclass(frozen=True, slots=True)
class FindCarmichaelView:
    interval_start: int
    interval_end: int
    carmichael_numbers: tuple[CarmichaelNumberView, ...]
    total_checked: int
