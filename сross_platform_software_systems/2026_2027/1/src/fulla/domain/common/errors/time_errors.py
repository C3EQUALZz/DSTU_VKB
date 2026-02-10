from fulla.domain.common.errors.base import DomainError


class InconsistentTimeError(DomainError):
    """Raised when updated_at is earlier than created_at."""

