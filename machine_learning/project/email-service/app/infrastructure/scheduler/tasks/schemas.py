from typing import Self, cast

from pydantic import BaseModel, Field, EmailStr, AnyHttpUrl

from app.domain.entities.user import UserEntity


class UserSendEmailForVerificationJobSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="User name for email")
    surname: str = Field(..., min_length=1, max_length=255, description="User surname for email")
    email: EmailStr = Field(..., description="Email address for sending verification email")
    url: AnyHttpUrl = Field(..., description="URL endpoint for verifying user. This url must be in email")

    @classmethod
    def from_(cls, entity: UserEntity) -> Self:
        return cls(
            name=entity.name.as_generic_type(),
            surname=entity.surname.as_generic_type(),
            email=cast(EmailStr, entity.email.as_generic_type()),
            url=cast(AnyHttpUrl, entity.url.as_generic_type()),
        )
