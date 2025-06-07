from pydantic import BaseModel


class MessageLLMSchema(BaseModel):
    chat_id: int
    content: str
