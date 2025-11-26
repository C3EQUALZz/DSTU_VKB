import contextlib
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from bazario import Notification


@dataclass(frozen=True, slots=True, eq=False)
class BaseDomainEvent(Notification):
    """
    Base event, from which any domain event should be inherited.
    Events represents internal operations, which may be executed.
    """

    event_id: UUID = field(
        init=False,
        kw_only=True,
        default_factory=lambda: uuid.uuid4(),
    )

    event_timestamp: datetime = field(
        init=False,
        kw_only=True,
        default_factory=lambda: datetime.now(UTC),
    )

    def to_dict(
        self,
        exclude: set[str] | None = None,
        include: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a dictionary representation of the model.

        Args:
            exclude: set of model fields, which should be excluded from.
            include: set of model fields, which should be included into.
        """

        data: dict[str, Any] = asdict(self)
        if exclude:
            for key in exclude:
                with contextlib.suppress(KeyError):
                    del data[key]

        if include:
            data.update(include)

        return data
