from typing import (
    List,
    Optional,
    Union,
)

from app.domain.entities.score import ScoreEntity
from app.exceptions.infrastructure import (
    AttributeException,
    ScoreNotFoundException,
)
from app.infrastructure.uow.scores.base import ScoresUnitOfWork


class ScoreService:
    def __init__(self, uow: ScoresUnitOfWork) -> None:
        self._uow = uow

    async def add(self, score: ScoreEntity) -> ScoreEntity:
        async with self._uow as uow:
            new_score: ScoreEntity = await uow.scores.add(score)
            await uow.commit()
            return new_score

    async def update(self, score: ScoreEntity) -> ScoreEntity:
        async with self._uow as uow:
            existing_score: Optional[ScoreEntity] = await uow.scores.get(score.oid)

            if not existing_score:
                raise ScoreNotFoundException(score.oid)

            updated_user = await uow.scores.update(oid=existing_score.oid, model=score)
            await uow.commit()
            return updated_user

    async def get_by_id(self, oid: str) -> ScoreEntity:
        async with self._uow as uow:
            user: Optional[ScoreEntity] = await uow.scores.get(oid=oid)
            if not user:
                raise ScoreNotFoundException(str(oid))

            return user

    async def get_all(self, page_number: int = 0, page_size: int = 10) -> List[ScoreEntity]:
        start: int = (page_number - 1) * page_size
        limit: int = start + page_size

        async with self._uow as uow:
            return await uow.scores.list(start=start, limit=limit)

    async def get_by_user_oid(self, user_oid: str) -> List[ScoreEntity]:
        async with self._uow as uow:
            scores: Optional[List[ScoreEntity]] = await uow.scores.get_by_user_oid(user_oid=user_oid)
            if not scores:
                raise ScoreNotFoundException(f"for user {user_oid}")

            return scores

    async def delete(self, oid: str) -> None:
        async with self._uow as uow:
            await uow.scores.delete(oid)
            await uow.commit()

    async def check_existence(
        self,
        oid: Optional[str] = None,
        user_oid: Optional[str] = None,
    ) -> bool:
        if not (oid or user_oid):
            raise AttributeException("oid or user_oid")
        async with self._uow as uow:
            score: Union[Optional[ScoreEntity], Optional[List[ScoreEntity]]]
            if oid:
                score = await uow.scores.get(oid=oid)
                if score:
                    return True

            if user_oid:
                score = await uow.scores.get_by_user_oid(user_oid=user_oid)
                if score:
                    return True

        return False
