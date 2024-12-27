from abc import abstractmethod, ABC
from typing import Optional, List

from app.domain.entities.score import ScoreEntity
from app.infrastructure.repositories.base import AbstractRepository


class ScoresRepository(AbstractRepository[ScoreEntity], ABC):
    """
    An interface for work with scores, that is used by scores unit of work.
    The main goal is that implementations of this interface can be easily replaced in scores unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_user_oid(self, user_oid: str, start: int = 0, limit: int = 10) -> Optional[List[ScoreEntity]]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: ScoreEntity) -> ScoreEntity:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: ScoreEntity) -> ScoreEntity:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, oid: str) -> ScoreEntity:
        raise NotImplementedError

    @abstractmethod
    async def list(self, start: int = 0, limit: int = 10) -> List[ScoreEntity]:
        raise NotImplementedError
