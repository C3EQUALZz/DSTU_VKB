from uuid import UUID

from pydantic import BaseModel, Field


class ChangeUsernameSchemaRequest(BaseModel):
    user_id: UUID = Field(
        ...,
        examples=[""],
        description="Unique user identifier from another service"
    )
    new_username: str = Field(
        ...,
        examples=["super_labuba"],
        min_length=1,
        description="user name in system"
    )
