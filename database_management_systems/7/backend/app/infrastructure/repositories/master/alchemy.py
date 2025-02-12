from sqlalchemy import Result, delete, select, Sequence, Row, RowMapping

from app.domain.entities.master import MasterEntity
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.master.base import MasterRepository
from typing import override, Optional, List, Any


class SQLAlchemyMasterRepository(SQLAlchemyAbstractRepository, MasterRepository):
    @override
    async def get_by_phone_number(self, number: str) -> Optional[MasterEntity]:
        raise NotImplementedError

    @override
    async def get_by_full_name(self, name: str, surname: str, patronymic: str):
        raise NotImplementedError

    @override
    async def add(self, model: MasterEntity) -> MasterEntity:
        raise NotImplementedError

    @override
    async def get(self, oid: str) -> Optional[MasterEntity]:
        raise NotImplementedError

    @override
    async def update(self, oid: str, model: MasterEntity) -> MasterEntity:
        raise NotImplementedError

    @override
    async def list(self, start: int = 0, limit: int = 10) -> List[MasterEntity]:
        result: Result = await self._session.execute(
            select(MasterEntity)
            .offset(start)
            .limit(limit)
        )

        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)

        for entity in trading_result_entities:
            assert isinstance(entity, MasterEntity)

        return trading_result_entities

    @override
    async def delete(self, oid: str) -> MasterEntity:
        result: Result = await self._session.execute(
            delete(MasterEntity)
            .filter_by(oid=oid)
            .returning(MasterEntity)
        )

        return result.scalar_one()
