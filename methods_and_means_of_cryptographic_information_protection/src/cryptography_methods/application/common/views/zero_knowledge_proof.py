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


