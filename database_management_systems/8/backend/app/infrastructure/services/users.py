from typing import (
    List,
    Optional,
)

from app.domain.entities.user import UserEntity
from app.infrastructure.exceptions import (
    AttributeException,
    UserNotFoundException,
)
from app.infrastructure.uow.users.base import UsersUnitOfWork


class UsersService:
    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow

    async def add(self, user: UserEntity) -> UserEntity:
        async with self._uow as uow:
            new_user: UserEntity = await uow.users.add(user)
            await uow.commit()
            return new_user

    async def get_by_email(self, email: str) -> UserEntity:
        async with self._uow as uow:
            user: Optional[UserEntity] = await uow.users.get_by_email(email)
            if not user:
                raise UserNotFoundException(email)

            return user

    async def update(self, user: UserEntity) -> UserEntity:
        async with self._uow as uow:
            existing_user: Optional[UserEntity] = await uow.users.get(user.oid)

            if not existing_user:
                raise UserNotFoundException(user.oid)

            updated_user = await uow.users.update(oid=existing_user.oid, model=user)
            await uow.commit()
            return updated_user

    async def get_by_name(self, name: str) -> UserEntity:
        async with self._uow as uow:
            user: Optional[UserEntity] = await uow.users.get_by_username(name)
            if not user:
                raise UserNotFoundException(name)

            return user

    async def get_by_id(self, oid: str) -> UserEntity:
        async with self._uow as uow:
            user: Optional[UserEntity] = await uow.users.get(oid=oid)
            if not user:
                raise UserNotFoundException(str(oid))

            return user

    async def get_all(self) -> List[UserEntity]:
        async with self._uow as uow:
            return await uow.users.list()

    async def delete(self, oid: str) -> None:
        async with self._uow as uow:
            await uow.users.delete(oid)
            await uow.commit()

    async def check_existence(
            self,
            oid: Optional[str] = None,
            email: Optional[str] = None,
            name: Optional[str] = None
    ) -> bool:
        if not (oid or email or name):
            raise AttributeException("oid or email or name")

        async with self._uow as uow:
            user: Optional[UserEntity]
            if oid:
                user = await uow.users.get(oid=oid)
                if user:
                    return True

            if email:
                user = await uow.users.get_by_email(email)
                if user:
                    return True

            if name:
                user = await uow.users.get_by_username(name)
                if user:
                    return True

        return False
