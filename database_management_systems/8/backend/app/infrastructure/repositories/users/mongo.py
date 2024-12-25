from typing import (
    List,
    Optional,
    override,
)

from app.domain.entities.user import UserEntity
from app.infrastructure.repositories.common.mongo import MotorAbstractRepository
from app.infrastructure.repositories.users.base import UsersRepository


class MotorUserRepository(UsersRepository, MotorAbstractRepository):
    @override
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        user = await self._collection.find_one(filter={"email": email})
        if user:
            return UserEntity.from_document(user)

    @override
    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        user = await self._collection.find_one(filter={"name": username})
        if user:
            return UserEntity.from_document(user)

    @override
    async def add(self, user: UserEntity) -> UserEntity:
        await self._collection.insert_one(user.to_dict())
        return user

    @override
    async def get(self, oid: str) -> Optional[UserEntity]:
        user = await self._collection.find_one(filter={"oid": oid})
        if user:
            return UserEntity.from_document(user)

    @override
    async def update(self, oid: str, model: UserEntity) -> UserEntity:
        update_data = model.to_dict()
        await self._collection.update_one({"oid": oid}, {"$set": update_data})
        return model

    @override
    async def delete(self, user_oid: str) -> Optional[UserEntity]:
        user = await self._collection.find_one_and_delete(filter={"oid": user_oid})
        if user:
            return UserEntity.from_document(user)

    @override
    async def list(self) -> List[UserEntity]:
        users = await self._collection.find().to_list(length=None)
        return [UserEntity.from_document(user) for user in users]
