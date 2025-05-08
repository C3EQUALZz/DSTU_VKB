from typing import Any, Sequence, override

from sqlalchemy import Result, Row, RowMapping, delete, insert, select, update

from app.domain.entities.user import UserEntity
from app.exceptions.infrastructure import TypeSignatureError
from app.infrastructure.repositories.database.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.database.users.base import UsersRepository


class SQLAlchemyUsersRepository(SQLAlchemyAbstractRepository, UsersRepository):

    @override
    async def get_all_by_name(self, name: str, start: int | None = None, limit: int | None = None) -> list[UserEntity]:
        raise NotImplementedError

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
        if (start is None) != (limit is None):
            raise TypeSignatureError("Both start and limit must be either None or both must be int.")

        if not (start is None and limit is None):
            result: Result = await self._session.execute(select(UserEntity))
        else:
            result: Result = await self._session.execute(select(UserEntity).offset(start).limit(limit))

        users: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(users, list)

        for entity in users:
            assert isinstance(entity, UserEntity)

        return users