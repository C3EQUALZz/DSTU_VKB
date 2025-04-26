from typing import Literal

from pydantic import BaseModel, Field

from app.application.api.v1.utils.schemas import StringUUID


class UserCreateSchemaEvent(BaseModel):
    oid: StringUUID = Field(..., description="UUID of user")
    first_name: str = Field(..., min_length=1, max_length=250, description="First name of the user, taken from telegram")
    role: Literal["bot", "user", "admin"] = Field(..., description="Role of the user")


class UserDeleteSchemaEvent(BaseModel):
    user_oid: StringUUID = Field(..., description="UUID of user")


class UserUpdateSchemaEvent(UserCreateSchemaEvent):
    ...
