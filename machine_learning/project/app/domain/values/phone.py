import re
from typing import override, Final

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import BadPhoneNumberError, BadVerificationStatusError

PHONE_NUMBER: Final[str] = r"^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$"


class PhoneNumber(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not re.match(PHONE_NUMBER, self.value):
            raise BadPhoneNumberError(f"Wrong phone number format {self.value}")

        if len(*filter(lambda n: n.isdigit(), self.value)) > 15:
            raise BadPhoneNumberError("Phone number length is too long")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


class VerificationStatus(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if self.value not in ("unverified", "verified"):
            raise BadVerificationStatusError(f"wrong provided status: {self.value}")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
