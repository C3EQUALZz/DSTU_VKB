from abc import ABC
from dataclasses import dataclass

from app.exceptions import ApplicationException


@dataclass(eq=False)
class DomainException(ApplicationException, ABC):
    @property
    def message(self) -> str:
        return "Exception on domain layer"


@dataclass(eq=False)
class EmptyTextException(DomainException):
    @property
    def message(self) -> str:
        return "Text is empty, please provide some information"


@dataclass(eq=False)
class ValueTooLongException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"Value it's to big {self.value[:30]}... Please provide shorter value"


@dataclass(eq=False)
class InvalidBookStatus(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"Invalid book status: {self.value}"


@dataclass(eq=False)
class BadNameFormatException(DomainException):
    value: str

    @property
    def message(self) -> str:
        return f"Bad name format: {self.value}"


@dataclass(eq=False)
class FakeYearException(DomainException):
    value: int

    @property
    def message(self) -> str:
        return f"Fake year {self.value}, please provide real year for book"


@dataclass(eq=False)
class ObsceneTextException(DomainException):
    text: str

    @property
    def message(self) -> str:
        return f"{self.text} is an obscene text"


@dataclass(eq=False)
class CastException(DomainException):
    text: str

    @property
    def message(self) -> str:
        return f"Failed to cast field {self.text}"