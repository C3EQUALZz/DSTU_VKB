from typing import Self, cast

from pydantic import BaseModel, EmailStr, Field

from app.domain.values.mail import Email


class EmailSchema(BaseModel):
    """
    Pydantic Email str can't be used without BaseModel class.
    So I created this class for validation for FastAPI mail.
    """
    value: EmailStr = Field(..., description="Email address")

    @classmethod
    def from_(cls, email_value_object: Email) -> Self:
        """
        Creating schema from given value object of email.
        :param email_value_object: value object of email.
        :return: Pydantic base model
        """
        return cls(
            value=cast(EmailStr, email_value_object.as_generic_type()),
        )
