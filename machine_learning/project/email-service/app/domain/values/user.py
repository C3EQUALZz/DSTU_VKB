import re
from dataclasses import dataclass
from typing import override, Pattern, AnyStr

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import EmptyFieldError, CantContainNumberFieldError, MalformedURL


@dataclass
class UserName(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Please provide a string value, not a %s", type(self.value))

        if self.value.isspace() or self.value == "":
            raise EmptyFieldError("Please provide a non-empty string value")

        if re.match(r"^*\d*$", self.value) is not None:
            raise CantContainNumberFieldError("String can't contain numbers, only alphas")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class UserSurname(UserName):
    ...


@dataclass
class UserURL(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Please provide a string value, not a %s", type(self.value))

        regex: Pattern[AnyStr] = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )

        if re.match(regex, self.value) is None:
            raise MalformedURL("Please provide a valid URL, not a %s" % self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
