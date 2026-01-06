from uuid import UUID

from pydantic import BaseModel, Field


class CreateUserSchemaRequest(BaseModel):
    user_id: UUID = Field(
        ...,
        examples=["a81bc81b-dead-4e5d-abff-90865d1e13b1"],
        description="User ID from other service"
    )
    user_name: str = Field(
        ...,
        examples=["super-puper-labuba"],
        description="User name from other service"
    )
