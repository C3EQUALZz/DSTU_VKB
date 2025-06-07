from pydantic import Field, BaseModel


class TextForSendToChatSchema(BaseModel):
    chat_id: int = Field(..., description="telegram chat id")
    content: str = Field(...)
