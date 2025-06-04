from typing import List, Optional

from app.domain.entities.user import UserEntity
from app.exceptions.infrastructure import UserNotFoundError
from app.infrastructure.uow.users.base import UsersUnitOfWork


class UsersService:
    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow

    def add(self, user: UserEntity) -> UserEntity:
        with self._uow as uow:
            new_user: UserEntity = uow.users.add(user)
            uow.commit()
            return new_user

    def update(self, user: UserEntity) -> UserEntity:
        with self._uow as uow:
            updated_user = uow.users.update(oid=user.oid, model=user)
            uow.commit()
            return updated_user

    def get_by_id(self, oid: str) -> UserEntity:
        with self._uow as uow:
            user: Optional[UserEntity] = uow.users.get(oid=oid)

            if not user:
                raise UserNotFoundError(str(oid))

            return user

    def get_by_email(self, email: str) -> UserEntity:
        with self._uow as uow:
            user: Optional[UserEntity] = uow.users.get_by_email(email)
            if not user:
                raise UserNotFoundError(email)

            return user

    def get_all(self, start: int | None = None, limit: int | None = None) -> List[UserEntity]:
        with self._uow as uow:
            return uow.users.list(start=start, limit=limit)

    def delete(self, oid: str) -> None:
        with self._uow as uow:
            uow.users.delete(oid)
            uow.commit()

    def check_existence(
            self,
            oid: Optional[str] = None,
            email: Optional[str] = None,
            surname: Optional[str] = None,
            name: Optional[str] = None,
    ) -> bool:
        if not (oid or email or (surname and name)):
            raise AttributeError("oid or email or full_name")

        with self._uow as uow:
            user: Optional[UserEntity]
            if oid:
                user = uow.users.get(oid=oid)
                if user:
                    return True

            if email:
                user = uow.users.get_by_email(email)
                if user:
                    return True

            if surname and name:
                user = uow.users.get_by_fullname(surname=surname, name=name)
                if user:
                    return True

        return False
