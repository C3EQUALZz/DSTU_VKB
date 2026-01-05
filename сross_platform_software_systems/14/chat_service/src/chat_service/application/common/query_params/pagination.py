from dataclasses import dataclass

from chat_service.application.errors.query_params import PaginationError


@dataclass(frozen=True, slots=True, kw_only=True)
class Pagination:
    offset: int | None = None
    limit: int | None = None

    def __post_init__(self) -> None:
        msg: str | None

        if self.offset is not None and self.offset < 0:
            msg = f"Limit must be greater than 0, got {self.limit}"
            raise PaginationError(msg)

        if self.limit is not None and self.limit <= 0:
            msg = f"Offset must be non-negative, got {self.offset}"
            raise PaginationError(msg)
