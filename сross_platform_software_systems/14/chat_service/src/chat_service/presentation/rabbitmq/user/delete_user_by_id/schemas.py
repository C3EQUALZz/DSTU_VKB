from uuid import UUID

from pydantic import BaseModel, Field


class DeleteUserByIDSchemaRequest(BaseModel):
    user_id: UUID = Field(
        ...,
        description="The user ID to delete",
        examples=["4f38774c-41ca-4019-9fe0-5490fd211084"]
    )
