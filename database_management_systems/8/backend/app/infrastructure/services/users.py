from typing import Optional, List

from app.domain.entities.user import UserEntity
from app.infrastructure.exceptions import AttributeException, UserNotFoundError
from app.infrastructure.uow.users.base import UsersUnitOfWork


class UsersService:
    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow

    async def create_user(self, user: UserEntity) -> UserEntity:
        async with self._uow as uow:
            new_user: UserEntity = await uow.users.add(user)
            await uow.commit()
            return new_user

    async def get_user_by_email(self, email: str) -> UserEntity:
        async with self._uow as uow:
            user: Optional[UserEntity] = await uow.users.get_by_email(email)
            if not user:
                raise UserNotFoundError(email)

            return user

    async def get_user_by_name(self, name: str) -> UserEntity:
        async with self._uow as uow:
            user: Optional[UserEntity] = await uow.users.get_by_username(name)
            if not user:
                raise UserNotFoundError(name)

            return user

    async def get_user_by_id(self, oid: str) -> UserEntity:
        async with self._uow as uow:
            user: Optional[UserEntity] = await uow.users.get(oid=oid)
            if not user:
                raise UserNotFoundError(str(oid))

            return user

    async def get_all_users(self) -> List[UserEntity]:
        async with self._uow as uow:
            users: List[UserEntity] = await uow.users.list()
            return users

    async def delete_user(self, oid: str) -> None:
        async with self._uow as uow:
            await uow.users.delete(oid)
            await uow.commit()

    async def check_user_existence(
            self, oid: Optional[str] = None,
            email: Optional[str] = None,
            name: Optional[str] = None
    ) -> bool:

        if not (oid or email or name):
            raise AttributeException

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
