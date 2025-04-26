import uuid

from sqlalchemy import TypeDecorator, String, Integer, UUID, Dialect
from typing import override
from app.domain.values.settings import TextModel, ImageModel
from app.domain.values.statistics import PositiveNumber
from app.domain.values.user import Role
from app.exceptions.infrastructure import ConvertingError


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


class TextModelDecorator(TypeDecorator):
    impl = String(50)
    cache_ok = True

    @override
    def process_bind_param(self, value: TextModel, dialect) -> str:
        if isinstance(value, TextModel):
            return value.as_generic_type()

        raise ConvertingError(
            f"Converting exception in sqlalchemy typedecorator has occurred."
            f" {self.__class__.__name__}, method: process_bind_param, value: {value}"
        )

    @override
    def process_result_value(self, value: str | None, dialect: Dialect) -> TextModel | None:
        return TextModel(value) if value else None


class ImageModelDecorator(TypeDecorator):
    impl = String(50)
    cache_ok = True

    @override
    def process_bind_param(self, value: ImageModel, dialect: Dialect) -> str:
        if isinstance(value, ImageModel):
            return value.as_generic_type()

        raise ConvertingError(
            f"Converting exception in sqlalchemy typedecorator has occurred."
            f" {self.__class__.__name__}, method: process_bind_param, value: {value}"
        )

    @override
    def process_result_value(self, value: str | None, dialect: Dialect) -> ImageModel | None:
        return ImageModel(value) if value else None


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


class PositiveNumberDecorator(TypeDecorator):
    impl = Integer
    cache_ok = True

    @override
    def process_bind_param(self, value: PositiveNumber, dialect: Dialect) -> int:
        if isinstance(value, PositiveNumber):
            return value.as_generic_type()

        raise ConvertingError(
            f"Converting exception in sqlalchemy typedecorator has occurred."
            f" {self.__class__.__name__}, method: process_bind_param, value: {value}"
        )

    @override
    def process_result_value(self, value: int, dialect: Dialect) -> PositiveNumber | None:
        return PositiveNumber(value) if value else None
