from dataclasses import dataclass

from chat_service.domain.chat.values.chat_id import ChatID
from chat_service.domain.chat.values.llm_provider import LLMProviderType
from chat_service.domain.chat.values.message_id import MessageID
from chat_service.domain.chat.values.message_role import MessageRole
from chat_service.domain.common.events import BaseDomainEvent
from chat_service.domain.user.values.user_id import UserID


@dataclass(frozen=True, slots=True, eq=False)
class MessageAppendedToChatEvent(BaseDomainEvent):
    chat_id: ChatID
    message_id: MessageID


@dataclass(frozen=True, slots=True, eq=False)
class UserChangedChatLLMProviderEvent(BaseDomainEvent):
    user_id: UserID
    selected_llm: LLMProviderType


@dataclass(frozen=True, slots=True, eq=False)
class MessageCreatedEvent(BaseDomainEvent):
    message_id: MessageID
    message_content: str
    sender_role: MessageRole


@dataclass(frozen=True, slots=True, eq=False)
class ChatCreatedEvent(BaseDomainEvent):
    chat_id: ChatID
    user_id: UserID
    selected_llm: LLMProviderType


@dataclass(frozen=True, slots=True, eq=False)
class MessageContentChangedEvent(BaseDomainEvent):
    message_id: MessageID
    message_content: str


@dataclass(frozen=True, slots=True, eq=False)
class MessageRoleChangedEvent(BaseDomainEvent):
    message_id: MessageID
    sender_role: MessageRole


@dataclass(frozen=True, slots=True, eq=False)
class MessageSuccessfullySentEvent(BaseDomainEvent):
    message_id: MessageID


@dataclass(frozen=True, slots=True, eq=False)
class MessageFailedSentEvent(BaseDomainEvent):
    message_id: MessageID
