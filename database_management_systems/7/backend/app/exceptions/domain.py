from app.exceptions.base import ApplicationException
from dataclasses import dataclass
from abc import ABC
from http import HTTPStatus


@dataclass(eq=False)
class DomainException(ApplicationException, ABC):
    @property
    def message(self) -> str:
        return "Exception on domain layer"

    @property
    def status(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class CastException(DomainException):
    text: str

    @property
    def message(self) -> str:
        return f"Failed to cast field {self.text}"


@dataclass(eq=False)
class BadFormatNumberException(DomainException):
    text: str

    @property
    def message(self) -> str:
        return f"Bad phone number {self.text}, please provide correct"


@dataclass(eq=False)
class BadSerialNumberException(DomainException):
    text: str

    @property
    def message(self) -> str:
        return f"Bad serial number {self.text}, please provide correct"


@dataclass(eq=False)
class BadPositionOfMasterException(DomainException):
    text: str

    @property
    def message(self) -> str:
        return f"Bad position of master {self.text}, please provide correct"


@dataclass(eq=False)
class HumanBadFullNameComponentException(DomainException):
    text: str

    @property
    def message(self) -> str:
        return f"Bad component of person full name {self.text}, please provide correct"


@dataclass(eq=False)
class MoneyCanNotBeNegativeException(DomainException):
    text: str

    @property
    def message(self) -> str:
        return f"Money can't be negative {self.text}, please provide correct"


