from mathematical_algorithms_of_geometry_in_cryptography.domain.common.errors.base import DomainError, DomainFieldError


class InvalidCurveParametersError(DomainFieldError):
    """Raised when curve parameters are invalid."""


class CurveGenerationError(DomainError):
    """Raised when curve generation fails."""


class PlotGenerationError(DomainError):
    """Raised when plot generation fails."""


