from abc import ABC
from dataclasses import (
    asdict,
    dataclass,
    field,
)
from datetime import datetime, UTC
from typing import (
    Any,
    Dict,
    get_type_hints,
    Optional,
    Set,
)
from uuid import uuid4

from app.exceptions.domain import CastException


@dataclass(eq=False)
class BaseEntity(ABC):
    """
    Base entity, from which any domain model should be inherited.
    """

    oid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)

    def __post_init__(self) -> None:
        for field_name, field_type in get_type_hints(self).items():
            if field_name == "oid":
                continue

            value = getattr(self, field_name, None)
            if not isinstance(value, field_type):
                try:
                    setattr(self, field_name, field_type(value))
                except (ValueError, TypeError):
                    raise CastException(f"'{field_name}' with value '{value}' to {field_type}")

    async def to_dict(
            self,
            exclude: Optional[Set[str]] = None,
            include: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a dictionary representation of the entity.

        exclude: set of model fields, which should be excluded from dictionary representation.
        include: set of model fields, which should be included into dictionary representation.
        """

        data: Dict[str, Any] = vars(self)

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
