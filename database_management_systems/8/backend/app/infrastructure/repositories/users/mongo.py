from typing import (
    List,
    Optional,
    override, Any, Mapping,
)

from motor.motor_asyncio import AsyncIOMotorCursor

from app.domain.entities.user import UserEntity
from app.infrastructure.repositories.common.mongo import MotorAbstractRepository
from app.infrastructure.repositories.users.base import UsersRepository


class MotorUsersRepository(UsersRepository, MotorAbstractRepository):
    @override
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        user = await self._collection.find_one(filter={"email": email})
        return UserEntity.from_document(user) if user else None

    @override
    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        user = await self._collection.find_one(filter={"name": username})
        return UserEntity.from_document(user) if user else None

    @override
    async def add(self, user: UserEntity) -> UserEntity:
        await self._collection.insert_one(user.to_dict())
        return user

    @override
    async def get(self, oid: str) -> Optional[UserEntity]:
        user = await self._collection.find_one(filter={"oid": oid})
        return UserEntity.from_document(user) if user else None

    @override
    async def update(self, oid: str, model: UserEntity) -> UserEntity:
        update_data = model.to_dict()
        await self._collection.update_one({"oid": oid}, {"$set": update_data})
        return model

    @override
    async def delete(self, user_oid: str) -> None:
        await self._collection.find_one_and_delete(filter={"oid": user_oid})

    @override
    async def list(self, start: int = 0, limit: int = 10) -> List[UserEntity]:
        users_cursor: AsyncIOMotorCursor[Any] = self._collection.find().skip(start).limit(limit)
        users: List[Mapping[str, Any]] = await users_cursor.to_list(length=limit)
        return [UserEntity.from_document(user) for user in users]
