"""Views для протокола идентификации с нулевой передачей данных."""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ZeroKnowledgeProofExecutionView:
    p: str
    q: str
    n: str
    v: str
    s: str
    total_iterations: int
    failed_attempts: int
    failure_rate: float
    authentication_passed: bool
    iterations: list[dict[str, int | str | bool | None]]


@dataclass(frozen=True, slots=True)
class ParallelZeroKnowledgeProofExecutionView:
    p: str
    q: str
    n: str
    k: int
    public_keys: list[str]   # V1, V2, ..., VK
    secret_keys: list[str]   # S1, S2, ..., SK
    total_iterations: int
    failed_attempts: int
    failure_rate: float
    cheat_probability: float  # (1/2)^(K*t)
    authentication_passed: bool
    iterations: list[dict[str, int | str | bool | None]]


