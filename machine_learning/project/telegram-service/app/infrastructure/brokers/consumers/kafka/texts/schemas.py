from pydantic import BaseModel


class MessageFromBrokerSchema(BaseModel):
    chat_id: int
    content: str
