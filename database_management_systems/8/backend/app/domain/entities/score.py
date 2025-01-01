from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    datetime,
    UTC,
)
from typing import (
    Any,
    Mapping,
    Self,
    Type,
)

from app.domain.entities.base import BaseEntity
from app.domain.values.scores import (
    ScoreValue,
    UserOID,
)


@dataclass(eq=False)
class ScoreEntity(BaseEntity):
    user_oid: UserOID
    value: ScoreValue
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    __eq__ = BaseEntity.__eq__
    __hash__ = BaseEntity.__hash__

    @classmethod
    def from_document(cls: Type[Self], document: Mapping[str, Any]) -> Self:
        oid: str = document["oid"]
        user_oid: UserOID = UserOID(document["user_oid"])
        value: ScoreValue = ScoreValue(document["value"])
        created_at: datetime = document["created_at"]

        return cls(
            oid=oid,
            user_oid=user_oid,
            value=value,
            created_at=created_at
        )
