from mathematical_algorithms_of_geometry_in_cryptography.domain.common.errors.base import DomainError, DomainFieldError


class InvalidNumberError(DomainFieldError):
    """Raised when a number does not meet the requirements for Pollard's Rho algorithm."""


class InvalidInitialValueError(DomainFieldError):
    """Raised when the initial value is invalid."""


class InvalidFunctionError(DomainFieldError):
    """Raised when the function expression is invalid."""


class DivisorNotFoundError(DomainError):
    """Raised when a divisor cannot be found (d == n)."""


class FunctionEvaluationError(DomainError):
    """Raised when function evaluation fails."""


