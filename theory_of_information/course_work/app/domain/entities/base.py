from abc import ABC
from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    UTC,
    datetime,
)
from typing import Any
from uuid import uuid4


@dataclass(eq=False)
class BaseEntity(ABC):
    """
    Base entity, from which any domain model should be inherited.
    """

    oid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)

    async def to_dict(
        self, exclude: set[str] | None = None, include: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Create a dictionary representation of the entity.

        exclude: set of model fields, which should be excluded from dictionary representation.
        include: set of model fields, which should be included into dictionary representation.
        """

        data: dict[str, Any] = vars(self)

        # For sqlalchemy
        data.pop("_sa_instance_state", None)

        # Handle exclude set
        if exclude:
            for key in exclude:
                data.pop(key, None)

        # Handle include dictionary
        if include:
            data.update(include)

        return data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            raise NotImplementedError
        return self.oid == other.oid

    def __hash__(self) -> int:
        return hash(self.oid)
