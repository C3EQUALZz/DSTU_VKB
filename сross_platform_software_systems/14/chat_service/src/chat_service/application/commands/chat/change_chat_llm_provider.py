import logging
from dataclasses import dataclass
from typing import final, Final
from uuid import UUID

from chat_service.application.common.ports.chat.chat_command_gateway import ChatCommandGateway
from chat_service.application.common.ports.chat.chat_query_gateway import ChatQueryGateway
from chat_service.application.common.ports.transaction_manager import TransactionManager
from chat_service.application.common.services.current_user_service import CurrentUserService
from chat_service.application.errors.chat import ChatNotFoundError
from chat_service.domain.chat.entities import Chat
from chat_service.domain.chat.services.chat_service import ChatService
from chat_service.domain.chat.values.chat_id import ChatID
from chat_service.domain.chat.values.llm_provider import LLMProviderType
from chat_service.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangeLLMProviderCommand:
    chat_id: UUID
    llm_provider: str


@final
class ChangeLLMProviderCommandHandler:
    def __init__(
            self,
            chat_service: ChatService,
            chat_query_gateway: ChatQueryGateway,
            chat_command_gateway: ChatCommandGateway,
            current_user_service: CurrentUserService,
            transaction_manager: TransactionManager,
    ) -> None:
        self._chat_service: Final[ChatService] = chat_service
        self._chat_query_gateway: Final[ChatQueryGateway] = chat_query_gateway
        self._chat_command_gateway: Final[ChatCommandGateway] = chat_command_gateway
        self._current_service: Final[CurrentUserService] = current_user_service
        self._transaction_manager: Final[TransactionManager] = transaction_manager

    async def __call__(self, data: ChangeLLMProviderCommand) -> None:
        logger.info(
            "Started changing llm provider: %s for chat with id: %s",
            data.llm_provider,
            data.chat_id
        )

        logger.info("Started reading current user")
        current_user: User = await self._current_service.get_current_user()
        logger.info("Got current user: %s", current_user)

        chat_id: ChatID = ChatID(data.chat_id)
        llm_provider: LLMProviderType = LLMProviderType(data.llm_provider)

        chat: Chat | None = await self._chat_query_gateway.read_by_id(
            chat_id
        )

        if chat is None:
            msg = f"Chat with id {chat_id} was not found"
            raise ChatNotFoundError(msg)

        self._chat_service.change_llm_provider(
            chat=chat,
            new_provider=llm_provider
        )

        await self._chat_command_gateway.update(chat=chat)
        await self._transaction_manager.commit()