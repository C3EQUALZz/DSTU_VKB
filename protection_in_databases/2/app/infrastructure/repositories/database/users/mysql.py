from typing import override

from app.domain.entities.user import UserEntity
from app.infrastructure.repositories.database.mysql import PyMySQLAbstractRepository
from app.infrastructure.repositories.database.users.base import UsersRepository


class PyMySQLUsersRepository(PyMySQLAbstractRepository, UsersRepository):
    @override
    def get_all_by_name(self, name: str, start: int | None = None, limit: int | None = None) -> list[UserEntity]:
        raise NotImplementedError

    @override
    def get_by_fullname(self, surname: str, name: str) -> UserEntity | None:
        ...

    @override
    def get_by_email(self, email: str) -> UserEntity | None:
        ...

    @override
    def add(self, model: UserEntity) -> UserEntity:
        ...

    @override
    def get(self, oid: str) -> UserEntity | None:
        ...

    @override
    def update(self, oid: str, model: UserEntity) -> UserEntity:
        ...

    @override
    def delete(self, oid: str) -> None:
        ...

    @override
    def list(self, start: int | None = None, limit: int | None = None) -> list[UserEntity]:
        ...
