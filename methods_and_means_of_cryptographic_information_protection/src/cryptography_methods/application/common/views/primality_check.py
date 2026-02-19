from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PrimalityCheckView:
    number: int
    is_prime: bool
    iterations: int
