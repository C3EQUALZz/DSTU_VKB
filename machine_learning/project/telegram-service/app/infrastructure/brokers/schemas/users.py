from typing import Literal

from pydantic import BaseModel, Field


class UserCreateSchema(BaseModel):
    id: int = Field(..., gt=0, description="user id in telegram")
    full_name: str = Field(min_length=1, max_length=100, description="full name of user in telegram")
    user_login: str = Field(min_length=1, max_length=100, description="login of user in telegram")
    role: Literal["admin", "user", "bot"] = Field(..., description="role of user in telegram")
    language_code: str = Field(default="ru", description="language of user in telegram")


class UserUpdateSchema(UserCreateSchema):
    ...


class UserDeleteSchema(BaseModel):
    id: int = Field(..., gt=0, description="user id in telegram")
