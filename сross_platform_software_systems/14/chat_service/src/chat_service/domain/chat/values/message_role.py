from enum import StrEnum


class MessageRole(StrEnum):
    """Role of the message sender."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"