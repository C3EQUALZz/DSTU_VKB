"""Domain errors for Fibonacci generator."""

from theory_of_pseudorandom_generators.domain.common.errors.base import DomainError


class WrongParameterValueError(DomainError):
    """Raised when a parameter has an invalid value."""



class WrongPolynomialDegreeError(DomainError):
    """Raised when polynomial degree doesn't match register length."""



class InvalidPolynomialAfterNormalizationError(DomainError):
    """Raised when polynomial after normalization is invalid."""



class ColumnIndexOutOfBoundsError(DomainError):
    """Raised when column index is out of register bounds."""



