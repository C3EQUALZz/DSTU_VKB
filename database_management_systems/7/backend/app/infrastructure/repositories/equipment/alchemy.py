from typing import Optional, override, List, Any

from sqlalchemy import Result, insert, select, update, delete, Sequence, Row, RowMapping

from app.domain.entities.equipment import EquipmentEntity
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.equipment.base import EquipmentRepository


class SQLAlchemyEquipmentRepository(SQLAlchemyAbstractRepository, EquipmentRepository):
    @override
    async def get_by_name_and_model(self, name: str, model: str) -> Optional[EquipmentEntity]:
        result: Result = await self._session.execute(
            select(EquipmentEntity)
            .filter_by(name=name, model=model)
        )

        return result.scalar_one_or_none()

    @override
    async def get_by_serial_number(self, serial_number: str) -> Optional[EquipmentEntity]:
        result: Result = await self._session.execute(
            select(EquipmentEntity)
            .filter_by(serial_number=serial_number)
        )

        return result.scalar_one_or_none()

    @override
    async def add(self, model: EquipmentEntity) -> EquipmentEntity:
        result: Result = await self._session.execute(
            insert(EquipmentEntity).values(**await model.to_dict()).returning(EquipmentEntity)
        )
        return result.scalar_one()

    @override
    async def get(self, oid: str) -> Optional[EquipmentEntity]:
        result: Result = await self._session.execute(select(EquipmentEntity).filter_by(oid=oid))

        return result.scalar_one_or_none()

    @override
    async def update(self, oid: str, model: EquipmentEntity) -> EquipmentEntity:
        result: Result = await self._session.execute(
            update(EquipmentEntity)
            .filter_by(oid=oid)
            .values(**await model.to_dict(exclude={"id"}))
            .returning(EquipmentEntity)
        )

        return result.scalar_one()

    @override
    async def delete(self, oid: str) -> EquipmentEntity:
        result: Result = await self._session.execute(
            delete(EquipmentEntity)
            .filter_by(oid=oid)
            .returning(EquipmentEntity)
        )

        return result.scalar_one()

    @override
    async def list(self, start: int = 0, limit: int = 10) -> List[EquipmentEntity]:
        result: Result = await self._session.execute(
            select(EquipmentEntity)
            .offset(start)
            .limit(limit)
        )

        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)

        for entity in trading_result_entities:
            assert isinstance(entity, EquipmentEntity)

        return trading_result_entities