from typing import (
    List,
    Optional,
)

from app.domain.entities.user import UserEntity
from app.exceptions.infrastructure import (
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
            updated_user = await uow.users.update(oid=user.oid, model=user)
            await uow.commit()
            return updated_user

    async def get_by_full_name(self, surname: str, name: str, patronymic: str) -> UserEntity:
        async with self._uow as uow:
            user: Optional[UserEntity] = await uow.users.get_by_fullname(
                surname=surname,
                name=name,
                patronymic=patronymic
            )

            if not user:
                raise UserNotFoundException(name)

            return user

    async def get_by_id(self, oid: str) -> UserEntity:
        async with self._uow as uow:
            user: Optional[UserEntity] = await uow.users.get(oid=oid)
            if not user:
                raise UserNotFoundException(str(oid))

            return user

    async def get_all(self, start: int = 0, limit: int = 10) -> List[UserEntity]:
        async with self._uow as uow:
            return await uow.users.list(start=start, limit=limit)

    async def delete(self, oid: str) -> None:
        async with self._uow as uow:
            await uow.users.delete(oid)
            await uow.commit()

    async def check_existence(
            self,
            oid: Optional[str] = None,
            email: Optional[str] = None,
            surname: Optional[str] = None,
            name: Optional[str] = None,
            patronymic: Optional[str] = None,
    ) -> bool:
        if not (oid or email or (surname and name and patronymic)):
            raise AttributeException("oid or email or full_name")

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

            if surname and name and patronymic:
                user = await uow.users.get_by_fullname(surname=surname, name=name, patronymic=patronymic)
                if user:
                    return True

        return False
