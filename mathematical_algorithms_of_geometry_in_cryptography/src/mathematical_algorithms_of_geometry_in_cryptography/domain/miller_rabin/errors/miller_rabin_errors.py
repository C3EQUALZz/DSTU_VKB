from mathematical_algorithms_of_geometry_in_cryptography.domain.common.errors.base import DomainError, DomainFieldError


class InvalidNumberError(DomainFieldError):
    """Raised when a number does not meet the requirements for Miller-Rabin test."""


class InvalidTestParametersError(DomainFieldError):
    """Raised when test parameters are invalid."""


class TestFailedError(DomainError):
    """Raised when a test iteration fails (number is composite)."""


class CantAddResultError(DomainFieldError):
    ...

