from dataclasses import dataclass, field

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

    def is_sent(self) -> bool:
        """Check if the message has been sent."""
        return self.status == MessageStatus.SENT

    def is_pending(self) -> bool:
        """Check if the message is pending."""
        return self.status == MessageStatus.PENDING

    def is_failed(self) -> bool:
        return self.status == MessageStatus.FAILED

