from typing import override

from app.domain.entities.user import UserEntity
from app.domain.values.user import Email, Password, Role
from app.infrastructure.repositories.database.mysql import PyMySQLAbstractRepository
from app.infrastructure.repositories.database.users.base import UsersRepository


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
            results = cursor.fetchall()
            return [
                UserEntity(
                    oid=row[0],
                    name=row[1],
                    surname=row[2],
                    email=Email(row[3]),
                    password=Password(row[4]),
                    role=Role(row[5]),
                    created_at=row[6],
                    updated_at=row[7]
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
            result = cursor.fetchone()

            if not result:
                return None

            return UserEntity(
                oid=result[0],
                name=result[1],
                surname=result[2],
                email=Email(result[3]),
                password=Password(result[4]),
                role=Role(result[5]),
                created_at=result[6],
                updated_at=result[7]
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
            result = cursor.fetchone()
            if not result:
                return None
            return UserEntity(
                oid=result[0],
                name=result[1],
                surname=result[2],
                email=Email(result[3]),
                password=Password(result[4]),
                role=Role(result[5]),
                created_at=result[6],
                updated_at=result[7]
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
            result = cursor.fetchone()

            if not result:
                return None

            return UserEntity(
                oid=result[0],
                name=result[1],
                surname=result[2],
                email=Email(result[3]),
                password=Password(result[4]),
                role=Role(result[5]),
                created_at=result[6],
                updated_at=result[7]
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
                    str(model.email),
                    model.password.value,
                    model.role.value,
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
            results = cursor.fetchall()
            return [
                UserEntity(
                    oid=row[0],
                    name=row[1],
                    surname=row[2],
                    email=Email(row[3]),
                    password=Password(row[4]),
                    role=Role(row[5]),
                    created_at=row[6],
                    updated_at=row[7]
                ) for row in results
            ]
