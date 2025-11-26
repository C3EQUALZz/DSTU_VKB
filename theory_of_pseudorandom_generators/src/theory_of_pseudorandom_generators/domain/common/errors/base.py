class AppError(Exception):
    """Base Error."""


class DomainError(AppError):
    """Base exception class for domain layer errors.

    Provides a consistent interface for error messages across all
        domain-specific.
    exceptions. All domain-level errors should inherit from this class.

    Note:
        - Serves as the root of the domain error hierarchy
        - Uses property decorator for consistent error message interface
        - Follows the convention of rich exceptions with additional attributes
    """


class DomainFieldError(DomainError):
    """
    Exception raised when domain field validation fails.

    Indicates that a value assigned to a domain object's field violates
    business rules or invariants.

    Note:
        - Inherits from DomainError to maintain consistent error handling
        - Used for validation failures in value objects and entities
        - Typically caught and converted to appropriate application errors
        - The default message from DomainError is usually sufficient,
          but can be overridden for specific field validation cases
    """
