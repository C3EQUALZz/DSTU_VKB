"""Domain errors for Geffe generator."""

from theory_of_pseudorandom_generators.domain.common.errors.base import DomainError


class PeriodsNotCoprimeError(DomainError):
    """Raised when register periods are not coprime."""



