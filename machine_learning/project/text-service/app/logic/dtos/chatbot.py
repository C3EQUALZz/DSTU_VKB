from dataclasses import dataclass


@dataclass(frozen=True)
class MessageAndChatIDDTO:
    content: str
    chat_id: int
