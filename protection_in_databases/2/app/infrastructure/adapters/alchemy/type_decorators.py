import uuid
from typing import override

from sqlalchemy import TypeDecorator, String, UUID, Dialect, LargeBinary

from app.domain.values.user import Role, Email, Password
from app.exceptions.infrastructure import ConvertingError


class EmailTypeDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    @override
    def process_bind_param(self, value: Email, dialect: Dialect) -> str:
        if value is not None:
            return value.as_generic_type()

        raise ConvertingError(f"{self.__class__.__name__}, method: process_bind_param, value: {value}")

    @override
    def process_result_value(self, column: str, dialect: Dialect) -> Email:
        if column is not None:
            return Email(column)

        raise ConvertingError(f"{self.__class__.__name__}, method: process_result_value, column: {column}")


class PasswordTypeDecorator(TypeDecorator):
    impl = LargeBinary
    cache_ok = True

    @override
    def process_bind_param(self, value: Password, dialect: Dialect) -> bytes:
        if value is not None:
            return value.as_generic_type()

        raise ConvertingError(f"{self.__class__.__name__}, method: process_bind_param, value: {value}")

    @override
    def process_result_value(self, column: bytes, dialect: Dialect) -> Password:
        if column is not None:
            return Password(column)
        raise ConvertingError(f"{self.__class__.__name__}, method: process_result_value, column: {column}")


class StringUUID(TypeDecorator):
    """Кастомный тип для преобразования UUID в строку при загрузке и строки в UUID при сохранении."""
    impl = UUID(as_uuid=True)
    cache_ok = True

    @override
    def process_bind_param(self, value: str, dialect: Dialect) -> UUID:
        if isinstance(value, str):
            return uuid.UUID(value)

        raise ConvertingError(
            f"Converting exception in sqlalchemy typedecorator has occurred."
            f" {self.__class__.__name__}, method: process_bind_param, value: {value}"
        )

    @override
    def process_result_value(self, value: UUID, dialect: Dialect) -> str:
        return str(value) if value else None


class RoleDecorator(TypeDecorator):
    impl = String(20)
    cache_ok = True

    @override
    def process_bind_param(self, value: Role, dialect: Dialect) -> str:
        if isinstance(value, Role):
            return value.as_generic_type()
        raise ConvertingError(
            f"Converting exception in sqlalchemy typedecorator has occurred."
            f" {self.__class__.__name__}, method: process_bind_param, value: {value}"
        )

    @override
    def process_result_value(self, value: str | None, dialect: Dialect) -> Role | None:
        return Role(value) if value else None
