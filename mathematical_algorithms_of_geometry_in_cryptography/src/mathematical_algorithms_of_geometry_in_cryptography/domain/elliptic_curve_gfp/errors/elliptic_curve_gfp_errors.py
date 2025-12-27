from mathematical_algorithms_of_geometry_in_cryptography.domain.common.errors.base import DomainError, DomainFieldError


class InvalidFieldParameterError(DomainFieldError):
    """Raised when field parameter is invalid (not prime)."""


class InvalidCurveParametersError(DomainFieldError):
    """Raised when curve parameters are invalid."""


class PointNotOnCurveError(DomainError):
    """Raised when a point does not belong to the curve."""


class CurveGenerationError(DomainError):
    """Raised when curve generation fails."""


class PointOperationError(DomainError):
    """Raised when point operation (addition/doubling) fails."""

