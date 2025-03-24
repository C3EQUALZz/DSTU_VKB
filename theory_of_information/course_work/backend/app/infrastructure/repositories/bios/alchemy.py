from typing import override, Sequence, Any

from sqlalchemy import delete, select, Result, Row, RowMapping, insert, update

from app.domain.entities.bio import BioEntity
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.bios.base import BiosRepository


class SQLAlchemyBiosRepository(SQLAlchemyAbstractRepository, BiosRepository):

    @override
    async def get_by_user_oid(self, user_id: str) -> BioEntity | None:
        result: Result = await self._session.execute(
            select(BioEntity).filter_by(user_id=user_id)
        )

        return result.scalar_one_or_none()

    @override
    async def add(self, model: BioEntity) -> BioEntity:
        result: Result = await self._session.execute(
            insert(BioEntity).values(**await model.to_dict()).returning(BioEntity)
        )

        return result.scalar_one()

    @override
    async def get(self, oid: str) -> BioEntity | None:
        result: Result = await self._session.execute(
            select(BioEntity).filter_by(oid=oid)
        )
        return result.scalar_one_or_none()

    @override
    async def update(self, oid: str, model: BioEntity) -> BioEntity:
        result: Result = await self._session.execute(
            update(BioEntity)
            .filter_by(oid=oid)
            .values(**await model.to_dict(exclude={"id"}))
            .returning(BioEntity)
        )

        return result.scalar_one()

    @override
    async def list(self, start: int = 0, limit: int = 10) -> list[BioEntity]:
        result: Result = await self._session.execute(select(BioEntity).offset(start).limit(limit))

        bio_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(bio_entities, list)

        for entity in bio_entities:
            assert isinstance(entity, BioEntity)

        return bio_entities

    @override
    async def delete(self, oid: str) -> None:
        await self._session.execute(delete(BioEntity).filter_by(id=id))
