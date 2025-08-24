from dataclasses import dataclass

from compressor.application.errors.query import PaginationError


@dataclass(frozen=True, slots=True, kw_only=True)
class Pagination:
    """
    raises PaginationError
    """

    limit: int
    offset: int

    def __post_init__(self) -> None:
        if self.limit <= 0:
            raise PaginationError(f"Limit must be greater than 0, got {self.limit}")
        if self.offset < 0:
            raise PaginationError(f"Offset must be non-negative, got {self.offset}")