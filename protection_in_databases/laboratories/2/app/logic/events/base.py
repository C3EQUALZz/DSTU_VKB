import contextlib
from abc import ABC
from dataclasses import (
    asdict,
    dataclass,
    field,
)
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class AbstractEvent(ABC):  # noqa
    """
    Base event, from which any domain event should be inherited.
    Events represents internal operations, which may be executed.
    """

    oid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)

    async def to_dict(self, exclude: set[str] | None = None, include: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Create a dictionary representation of the model.

        exclude: set of model fields, which should be excluded from dictionary representation.
        include: set of model fields, which should be included into dictionary representation.
        """

        data: dict[str, Any] = asdict(self)
        if exclude:
            for key in exclude:
                with contextlib.suppress(KeyError):
                    del data[key]

        if include:
            data.update(include)

        return data
