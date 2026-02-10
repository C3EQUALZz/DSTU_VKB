class DomainError(Exception):
    """Base exception for all domain-level errors."""


class DomainFieldError(DomainError):
    """Raised when a domain field constraint is violated."""


