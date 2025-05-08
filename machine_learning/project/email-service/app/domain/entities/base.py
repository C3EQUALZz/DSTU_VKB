from abc import ABC
from dataclasses import asdict, dataclass, field, fields
from datetime import UTC, datetime
from typing import Any, Dict, Optional, Set
from uuid import uuid4


@dataclass(eq=False)
class BaseEntity(ABC):
    """
    Base entity, from which any domain model should be inherited.
    """

    oid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC), kw_only=True
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC), kw_only=True
    )

    async def to_dict(
            self,
            exclude: Optional[Set[str]] = None,
            include: Optional[Dict[str, Any]] = None,
            save_classes_value_objects: bool = True,
    ) -> Dict[str, Any]:
        """
        Create a dictionary representation of the entity.

        exclude: set of model fields, which should be excluded from dictionary representation.
        include: set of model fields, which should be included into dictionary representation.
        """

        if save_classes_value_objects:
            data: Dict[str, Any] = vars(self)
        else:
            data: Dict[str, Any] = asdict(self)

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

    def set_attrs(
            self,
            updated_attrs: Dict[str, Any],
    ) -> None:
        valid_attrs = {f.name for f in fields(self)}
        for attr, value in updated_attrs.items():
            if value is None:
                continue
            if attr not in valid_attrs:
                raise ValueError("Invalid attribute: %s, all attrs is here: %s", attr, valid_attrs)

            current_value = getattr(self, attr)
            if hasattr(current_value, "value"):  # Проверка Value Object
                setattr(self, attr, type(current_value)(value))
            else:
                if type(value) != type(current_value):
                    raise TypeError(f"Type mismatch for {attr}")
                setattr(self, attr, value)

        self.updated_at = datetime.now(UTC)  # Обновляем только при реальных изменениях
