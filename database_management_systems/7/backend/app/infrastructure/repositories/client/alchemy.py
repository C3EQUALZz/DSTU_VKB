from app.domain.entities.client import ClientEntity
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.client.base import ClientRepository
from typing import override, Optional, List, Any
from sqlalchemy import select, Result, insert, delete, Sequence, Row, RowMapping, update


class SQLAlchemyClientRepository(SQLAlchemyAbstractRepository, ClientRepository):
    @override
    async def get_by_full_name(self, name: str, surname: str, patronymic: str):
        result: Result = await self._session.execute(
            select(ClientEntity)
            .filter_by(
                name=name,
                surname=surname,
                patronymic=patronymic,
            )
        )

        return result.scalar_one_or_none()

    @override
    async def add(self, model: ClientEntity) -> ClientEntity:
        result: Result = await self._session.execute(
            insert(ClientEntity).values(**await model.to_dict()).returning(ClientEntity)
        )
        return result.scalar_one()

    @override
    async def get(self, oid: str) -> Optional[ClientEntity]:
        result: Result = await self._session.execute(select(ClientEntity).filter_by(oid=oid))

        return result.scalar_one_or_none()

    @override
    async def update(self, oid: str, model: ClientEntity) -> ClientEntity:
        result: Result = await self._session.execute(
            update(ClientEntity)
            .filter_by(oid=oid)
            .values(**await model.to_dict(exclude={"id"}))
            .returning(ClientEntity)
        )

        return result.scalar_one()

    @override
    async def list(self, start: int = 0, limit: int = 10) -> List[ClientEntity]:
        result: Result = await self._session.execute(
            select(ClientEntity)
            .offset(start)
            .limit(limit)
        )

        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)

        for entity in trading_result_entities:
            assert isinstance(entity, ClientEntity)

        return trading_result_entities

    @override
    async def delete(self, oid: str) -> ClientEntity:
        result: Result = await self._session.execute(
            delete(ClientEntity)
            .filter_by(oid=oid)
            .returning(ClientEntity)
        )

        return result.scalar_one()
