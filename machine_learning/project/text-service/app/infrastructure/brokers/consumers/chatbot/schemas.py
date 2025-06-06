from pydantic import BaseModel


class TextToChatBotSchema(BaseModel):
    chat_id: int
    content: str
