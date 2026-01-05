from enum import StrEnum


class MessageStatus(StrEnum):
    """Status of the message."""

    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
