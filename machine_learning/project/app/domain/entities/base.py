from abc import ABC
from dataclasses import (
    asdict,
    dataclass,
    field,
)
from datetime import (
    UTC,
    datetime,
)
from typing import (
    Any,
    Optional,
)
from uuid import uuid4


@dataclass(eq=False)
class BaseEntity(ABC):  # noqa
    """
    Base entity, from which any domain model should be inherited.
    """

    oid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)

    async def to_dict(
        self,
        exclude: Optional[set[str]] = None,
        include: Optional[dict[str, Any]] = None,
        save_classes_value_objects: bool = False,
    ) -> dict[str, Any]:
        """
        Create a dictionary representation of the entity.

        exclude: set of model fields, which should be excluded from dictionary representation.
        include: set of model fields, which should be included into dictionary representation.
        """

        if save_classes_value_objects:
            data: dict[str, Any] = vars(self)
        else:
            data: dict[str, Any] = asdict(self)

            for key, value in data.items():
                if isinstance(value, dict) and "value" in value:
                    data[key] = value["value"]

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
