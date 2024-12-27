from typing import override, Optional, Any, Mapping, List

from motor.motor_asyncio import AsyncIOMotorCursor

from app.domain.entities.score import ScoreEntity
from app.infrastructure.repositories.common.mongo import MotorAbstractRepository
from app.infrastructure.repositories.scores.base import ScoresRepository


class MotorScoresRepository(ScoresRepository, MotorAbstractRepository):
    @override
    async def get_by_user_oid(self, user_oid: str, start: int = 0, limit: int = 10) -> Optional[List[ScoreEntity]]:
        scores_cursor: AsyncIOMotorCursor[Any] = self._collection.find().skip(start).limit(limit)
        scores: List[Mapping[str, Any]] = await scores_cursor.to_list(length=limit)
        if scores is None:
            return None
        return [ScoreEntity.from_document(score) for score in scores]

    @override
    async def add(self, score: ScoreEntity) -> ScoreEntity:
        await self._collection.insert_one(score.to_dict())
        return score

    @override
    async def get(self, oid: str) -> Optional[ScoreEntity]:
        user = await self._collection.find_one(filter={"oid": oid})
        return ScoreEntity.from_document(user) if user else None

    @override
    async def update(self, oid: str, model: ScoreEntity) -> ScoreEntity:
        update_data = model.to_dict()
        await self._collection.update_one({"oid": oid}, {"$set": update_data})
        return model

    @override
    async def delete(self, score_oid: str) -> None:
        await self._collection.find_one_and_delete(filter={"oid": score_oid})

    @override
    async def list(self, start: int = 0, limit: int = 10) -> List[ScoreEntity]:
        scores_cursor: AsyncIOMotorCursor[Any] = self._collection.find().skip(start).limit(limit)
        scores: List[Mapping[str, Any]] = await scores_cursor.to_list(length=limit)
        return [ScoreEntity.from_document(user) for user in scores]
