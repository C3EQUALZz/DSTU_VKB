from typing import override, Sequence, Any

from sqlalchemy import Result, select, delete, Row, RowMapping, insert, update

from app.domain.entities.user import UserEntity
from app.domain.values.user import Email
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.users.base import UsersRepository


class SQLAlchemyUsersRepository(SQLAlchemyAbstractRepository, UsersRepository):

    @override
    async def get_by_fullname(self, surname: str, name: str, patronymic: str) -> UserEntity | None:
        result: Result = await self._session.execute(
            select(UserEntity).filter_by(
                surname=surname,
                name=name,
                patronymic=patronymic
            )
        )

        return result.scalar_one_or_none()

    @override
    async def get_by_email(self, email: str) -> UserEntity | None:
        result: Result = await self._session.execute(
            select(UserEntity).filter_by(email=Email(email))
        )

        return result.scalar_one_or_none()

    @override
    async def add(self, model: UserEntity) -> UserEntity:
        result: Result = await self._session.execute(
            insert(UserEntity).values(**await model.to_dict()).returning(UserEntity)
        )
        return result.scalar_one()

    @override
    async def get(self, oid: str) -> UserEntity | None:
        result: Result = await self._session.execute(
            select(UserEntity).filter_by(oid=oid)
        )

        return result.scalar_one_or_none()

    @override
    async def update(self, oid: str, model: UserEntity) -> UserEntity:
        result: Result = await self._session.execute(
            update(UserEntity)
            .filter_by(oid=oid)
            .values(**await model.to_dict(exclude={"oid"}))
            .returning(UserEntity)
        )

        return result.scalar_one()

    @override
    async def delete(self, oid: str) -> None:
        await self._session.execute(delete(UserEntity).filter_by(oid=oid))

    @override
    async def list(self, start: int = 0, limit: int = 10) -> list[UserEntity]:
        result: Result = await self._session.execute(select(UserEntity).offset(start).limit(limit))

        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)

        for entity in trading_result_entities:
            assert isinstance(entity, UserEntity)

        return trading_result_entities
