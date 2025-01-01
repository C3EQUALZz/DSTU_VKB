from datetime import datetime
from typing import Self

from pydantic import BaseModel

from app.domain.entities.score import ScoreEntity


class CreateScoreSchemeRequest(BaseModel):
    user_id: str
    value: int


class GetAllScoreSchemeRequest(BaseModel):
    page_number: int
    page_size: int


class ScoreSchemeResponse(BaseModel):
    value: int
    user_oid: str
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: ScoreEntity) -> Self:
        return cls(
            value=entity.value.as_generic_type(),
            user_oid=entity.user_oid.as_generic_type(),
            created_at=entity.created_at
        )
