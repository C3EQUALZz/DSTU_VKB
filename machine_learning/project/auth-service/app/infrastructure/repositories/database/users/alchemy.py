from typing import Any, Sequence, override

from sqlalchemy import Result, Row, RowMapping, delete, insert, select, update

from app.domain.entities.user import UserEntity
from app.domain.values.user import UserEmail
from app.infrastructure.repositories.database.alchemy import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.database.users.base import UsersRepository


class SQLAlchemyUsersRepository(SQLAlchemyAbstractRepository, UsersRepository):
    @override
    async def get_by_fullname(self, surname: str, name: str) -> UserEntity | None:
        result: Result = await self._session.execute(
            select(UserEntity).filter_by(surname=surname, name=name)
        )
        return result.scalar_one_or_none()

    @override
    async def get_by_email(self, email: str) -> UserEntity | None:
        result: Result = await self._session.execute(select(UserEntity).filter_by(email=UserEmail(email)))
        return result.scalar_one_or_none()

    @override
    async def add(self, model: UserEntity) -> UserEntity:
        result: Result = await self._session.execute(
            insert(UserEntity).values(**await model.to_dict()).returning(UserEntity)
        )
        return result.scalar_one()

    @override
    async def get(self, oid: str) -> UserEntity | None:
        result: Result = await self._session.execute(select(UserEntity).filter_by(oid=oid))

        return result.scalar_one_or_none()

    @override
    async def update(self, oid: str, model: UserEntity) -> UserEntity:
        result: Result = await self._session.execute(
            update(UserEntity).filter_by(oid=oid).values(**await model.to_dict(exclude={"oid"})).returning(UserEntity)
        )

        return result.scalar_one()

    @override
    async def delete(self, oid: str) -> None:
        await self._session.execute(delete(UserEntity).filter_by(oid=oid))

    @override
    async def list(self, start: int | None = None, limit: int | None = None) -> list[UserEntity]:
        result: Result[tuple[UserEntity]]

        if start is not None and limit is not None:
            result = await self._session.execute(select(UserEntity).offset(start).limit(limit))
        else:
            result = await self._session.execute(select(UserEntity))

        entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(entities, list)

        for entity in entities:
            assert isinstance(entity, UserEntity)

        return entities
