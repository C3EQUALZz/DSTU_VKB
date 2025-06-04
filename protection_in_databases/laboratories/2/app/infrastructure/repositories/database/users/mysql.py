import logging
from typing import override, Final, Any, cast

from app.domain.entities.user import UserEntity
from app.domain.values.user import Email, Password, Role
from app.infrastructure.repositories.database.mysql import PyMySQLAbstractRepository
from app.infrastructure.repositories.database.users.base import UsersRepository

logger: Final[logging.Logger] = logging.getLogger(__name__)

class PyMySQLUsersRepository(PyMySQLAbstractRepository, UsersRepository):
    @override
    def get_all_by_name(self, name: str, start: int | None = None, limit: int | None = None) -> list[UserEntity]:
        query: str = "SELECT id, name, surname, email, password, role, created_at, updated_at FROM users WHERE name = %s"
        params = [name]
        if limit:
            query += " LIMIT %s"
            params.append(limit)
        if start:
            query += " OFFSET %s"
            params.append(start)

        with self._connection.cursor() as cursor:
            cursor.execute(query, params)
            results: list[dict[str, Any]] = cast(list[dict[str, Any]], cursor.fetchall())

            return [
                UserEntity(
                    oid=row["id"],
                    name=row["name"],
                    surname=row["surname"],
                    email=Email(row["email"]),
                    password=Password(row["password"]),
                    role=Role(row["role"]),
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                ) for row in results
            ]

    @override
    def get_by_fullname(self, surname: str, name: str) -> UserEntity | None:
        query: str = """
        SELECT id, name, surname, email, password, role, created_at, updated_at
        FROM users
        WHERE name = %s AND surname = %s
        LIMIT 1
        """
        with self._connection.cursor() as cursor:
            cursor.execute(query, (name, surname))
            result: dict[str, Any] = cast(dict[str, Any], cursor.fetchone())

            if not result:
                return None

            return UserEntity(
                oid=result["id"],
                name=result["name"],
                surname=result["surname"],
                email=Email(result["email"]),
                password=Password(result["password"]),
                role=Role(result["role"]),
                created_at=result["created_at"],
                updated_at=result["updated_at"]
            )

    @override
    def get_by_email(self, email: str) -> UserEntity | None:
        query = """
        SELECT id, name, surname, email, password, role, created_at, updated_at
        FROM users
        WHERE email = %s
        LIMIT 1
        """

        with self._connection.cursor() as cursor:
            cursor.execute(query, (email,))
            result: dict[str, Any] = cast(dict[str, Any], cursor.fetchone())

            if not result:
                return None

            return UserEntity(
                oid=result["id"],
                name=result["name"],
                surname=result["surname"],
                email=Email(result["email"]),
                password=Password(result["password"]),
                role=Role(result["role"]),
                created_at=result["created_at"],
                updated_at=result["updated_at"]
            )

    @override
    def add(self, model: UserEntity) -> UserEntity:
        query: str = """
        INSERT INTO users (id, name, surname, email, password, role, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        with self._connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    model.oid,
                    model.name,
                    model.surname,
                    model.email.as_generic_type(),
                    model.password.as_generic_type(),
                    model.role.as_generic_type(),
                    model.created_at,
                    model.updated_at
                )
            )
        return model

    @override
    def get(self, oid: str) -> UserEntity | None:
        query: str = """
        SELECT id, name, surname, email, password, role, created_at, updated_at
        FROM users
        WHERE id = %s
        LIMIT 1
        """

        with self._connection.cursor() as cursor:
            cursor.execute(query, (oid,))
            result: dict[str, Any] = cast(dict[str, Any], cursor.fetchone())

            if not result:
                return None

            return UserEntity(
                oid=result["id"],
                name=result["name"],
                surname=result["surname"],
                email=Email(result["email"]),
                password=Password(result["password"]),
                role=Role(result["role"]),
                created_at=result["created_at"],
                updated_at=result["updated_at"]
            )

    @override
    def update(self, oid: str, model: UserEntity) -> UserEntity:
        query = """
        UPDATE users
        SET name = %s, surname = %s, email = %s, password = %s, role = %s, updated_at = NOW()
        WHERE id = %s
        """
        with self._connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    model.name,
                    model.surname,
                    model.email.as_generic_type(),
                    model.password.as_generic_type(),
                    model.role.as_generic_type(),
                    oid
                )
            )

        return model

    @override
    def delete(self, oid: str) -> None:
        query: str = "DELETE FROM users WHERE id = %s"
        with self._connection.cursor() as cursor:
            cursor.execute(query, (oid,))

    @override
    def list(self, start: int | None = None, limit: int | None = None) -> list[UserEntity]:
        query: str = "SELECT id, name, surname, email, password, role, created_at, updated_at FROM users"
        params = []
        if limit:
            query += " LIMIT %s"
            params.append(limit)
        if start:
            query += " OFFSET %s"
            params.append(start)

        with self._connection.cursor() as cursor:
            cursor.execute(query, params)
            results: list[dict[str, Any]] = cast(list[dict[str, Any]], cursor.fetchall())

            logger.info(results)

            return [
                UserEntity(
                    oid=row["id"],
                    name=row["name"],
                    surname=row["surname"],
                    email=Email(row["email"]),
                    password=Password(row["password"]),
                    role=Role(row["role"]),
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                ) for row in results
            ]
