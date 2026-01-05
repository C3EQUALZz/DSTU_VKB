from dataclasses import dataclass, field
from datetime import datetime, UTC

from chat_service.domain.chat.values.message_content import MessageContent
from chat_service.domain.chat.values.message_id import MessageID
from chat_service.domain.chat.values.message_role import MessageRole
from chat_service.domain.chat.values.message_status import MessageStatus
from chat_service.domain.common.entities.base_entity import BaseEntity


@dataclass(eq=False, kw_only=True)
class Message(BaseEntity[MessageID]):
    """Entity representing a message in a chat.

    Messages are part of the Chat aggregate and represent
    individual messages in the conversation history.
    """

    content: MessageContent
    role: MessageRole = MessageRole.USER
    status: MessageStatus = field(default=MessageStatus.PENDING)

    def mark_as_sent(self) -> None:
        """Mark the message as successfully sent."""
        self.status = MessageStatus.SENT
        self.updated_at = datetime.now(UTC)

    def mark_as_failed(self) -> None:
        """Mark the message as failed."""
        self.status = MessageStatus.FAILED
        self.updated_at = datetime.now(UTC)

    def is_sent(self) -> bool:
        """Check if the message has been sent."""
        return self.status == MessageStatus.SENT

    def is_pending(self) -> bool:
        """Check if the message is pending."""
        return self.status == MessageStatus.PENDING
