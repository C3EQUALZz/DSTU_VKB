from dataclasses import dataclass, field

from chat_service.domain.chat.entities.message import Message
from chat_service.domain.chat.values.chat_id import ChatID
from chat_service.domain.chat.values.llm_provider import LLMProviderType
from chat_service.domain.common.entities.base_aggregate import BaseAggregateRoot
from chat_service.domain.user.entities.user import User


@dataclass(eq=False, repr=False)
class Chat(BaseAggregateRoot[ChatID]):
    """Chat aggregate root.

    Represents a chat session with a selected LLM provider.
    Contains the conversation history (messages) and access token
    for external access to the chat.
    """

    user: User
    selected_llm: LLMProviderType = field(default_factory=LLMProviderType.QWEN_3_CODER)
    messages: list[Message] = field(default_factory=list)

    def get_messages(self) -> list[Message]:
        """Get all messages in chronological order."""
        return sorted(self.messages, key=lambda m: m.created_at)

    def get_last_message(self) -> Message | None:
        """Get the last message in the chat."""
        if not self.messages:
            return None
        return max(self.messages, key=lambda m: m.created_at)
