import logging
from datetime import datetime, UTC
from typing import Final

from chat_service.domain.chat.entities import Chat, Message
from chat_service.domain.chat.events import (
    MessageAppendedToChatEvent,
    UserChangedChatLLMProviderEvent,
    ChatCreatedEvent
)
from chat_service.domain.chat.ports.chat_id_generator import ChatIDGenerator
from chat_service.domain.chat.values.chat_id import ChatID
from chat_service.domain.chat.values.llm_provider import LLMProviderType
from chat_service.domain.common.services.base import DomainService
from chat_service.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


class ChatService(DomainService):
    def __init__(
            self,
            chat_id_generator: ChatIDGenerator,
    ) -> None:
        super().__init__()
        self._chat_id_generator: Final[ChatIDGenerator] = chat_id_generator

    def create(
            self,
            user: User,
            selected_llm: LLMProviderType | None = None,
    ) -> Chat:
        logger.debug(
            "Started creating new chat for user %s with selected llm: %s",
            user.id,
            selected_llm
        )

        new_chat_id: ChatID = self._chat_id_generator()

        logger.debug("Generated new chat id: %s", new_chat_id)

        new_chat: Chat = Chat(
            id=new_chat_id,
            user=user,
            selected_llm=selected_llm if selected_llm is not None else LLMProviderType.QWEN_3_CODER,
        )

        new_event: ChatCreatedEvent = ChatCreatedEvent(
            chat_id=new_chat_id,
            user_id=user.id,
            selected_llm=new_chat.selected_llm
        )

        self._record_event(new_event)

        logger.debug(
            "Generated new event: %s",
            new_event
        )

        return new_chat

    def add_message(self, chat: Chat, message: Message) -> None:
        """Add a message to the chat history."""
        logger.debug(
            "Started adding message %s for chat with id %s",
            message,
            chat.id
        )

        chat.messages.append(message)
        chat.updated_at = datetime.now(UTC)

        new_event: MessageAppendedToChatEvent = MessageAppendedToChatEvent(
            chat_id=chat.id,
            message_id=message.id,
        )

        self._record_event(new_event)

        logger.debug(
            "Create new chat event: %s",
            new_event
        )

    def change_llm_provider(self, chat: Chat, new_provider: LLMProviderType) -> None:
        """Change the selected LLM provider."""
        logger.debug(
            "Started changing llm provider %s for chat with id %s",
            new_provider,
            chat.id
        )

        chat.selected_llm = new_provider
        chat.updated_at = datetime.now(UTC)

        new_event: UserChangedChatLLMProviderEvent = UserChangedChatLLMProviderEvent(
            user_id=chat.user.id,
            selected_llm=chat.selected_llm,
        )

        self._record_event(new_event)

        logger.debug(
            "Create new chat event: %s",
            new_event
        )
