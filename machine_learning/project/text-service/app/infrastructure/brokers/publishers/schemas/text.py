from pydantic import BaseModel


class ReplyFromLLMToChatSchema(BaseModel):
    content: str
    chat_id: int
