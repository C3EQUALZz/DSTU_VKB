from sqlalchemy import TypeDecorator, String, Dialect, LargeBinary

from app.domain.values.bio import PhoneNumber, Gender
from app.domain.values.shared import URL
from app.domain.values.user import Email, Password, Status, Role
from app.exceptions.infrastructure import ConvertingException


class PhoneNumberTypeDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: PhoneNumber, dialect: Dialect) -> str:
        if value is not None and isinstance(value, PhoneNumber):
            return value.as_generic_type()

        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, value: {value}")

    def process_result_value(self, column: str, dialect: Dialect) -> PhoneNumber:
        if column is not None:
            return PhoneNumber(column)
        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")


class EmailTypeDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: Email, dialect: Dialect) -> str:
        if value is not None:
            return value.as_generic_type()

        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, value: {value}")

    def process_result_value(self, column: str, dialect: Dialect) -> Email:
        if column is not None:
            return Email(column)

        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")


class PasswordTypeDecorator(TypeDecorator):
    impl = LargeBinary
    cache_ok = True

    def process_bind_param(self, value: Password, dialect: Dialect) -> bytes:
        if value is not None:
            return value.as_generic_type()

        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, value: {value}")

    def process_result_value(self, column: bytes, dialect: Dialect) -> Password:
        if column is not None:
            return Password(column)
        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")


class GenderTypeDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: Gender, dialect: Dialect) -> str:
        if value is not None:
            return value.as_generic_type()
        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, value: {value}")

    def process_result_value(self, column: str, dialect: Dialect) -> Gender:
        if column is not None:
            return Gender(column)
        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")

class StatusDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: Status, dialect: Dialect) -> str:
        if value is not None:
            return value.as_generic_type()

        if value is not None and isinstance(value, str):
            return value

        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, value: {value}")

    def process_result_value(self, column: str, dialect: Dialect) -> Status:
        if column is not None:
            return Status(column)

        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")

class RoleDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: Role, dialect: Dialect) -> str:
        if value is not None:
            return value.as_generic_type()

        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, value: {value}")

    def process_result_value(self, column: str, dialect: Dialect) -> Role:
        if column is not None:
            return Role(column)
        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")


class URLTypeDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: URL, dialect: Dialect) -> str:
        if value is not None:
            return value.as_generic_type()
        raise ConvertingException(f"{self.__class__.__name__}, method: process_bind_param, value: {value}")

    def process_result_value(self, column: str, dialect: Dialect) -> URL:
        if column is not None:
            return URL(column)
        raise ConvertingException(f"{self.__class__.__name__}, method: process_result_value, column: {column}")