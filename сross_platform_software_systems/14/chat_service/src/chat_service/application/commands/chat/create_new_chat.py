import logging
from dataclasses import dataclass
from typing import final, Final

from chat_service.application.common.ports.chat.chat_command_gateway import ChatCommandGateway
from chat_service.application.common.ports.event_bus import EventBus
from chat_service.application.common.ports.transaction_manager import TransactionManager
from chat_service.application.common.services.current_user_service import CurrentUserService
from chat_service.application.common.views.chat.create_chat_view import CreateChatView
from chat_service.domain.chat.entities import Chat
from chat_service.domain.chat.services.chat_service import ChatService
from chat_service.domain.chat.values.llm_provider import LLMProviderType
from chat_service.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateNewChatCommand:
    llm_provider: str | None = None


@final
class CreateNewChatCommandHandler:
    def __init__(
            self,
            chat_command_gateway: ChatCommandGateway,
            transaction_manager: TransactionManager,
            chat_service: ChatService,
            event_bus: EventBus,
            current_user_service: CurrentUserService,
    ) -> None:
        self._chat_service: Final[ChatService] = chat_service
        self._chat_command_gateway: Final[ChatCommandGateway] = chat_command_gateway
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._event_bus: Final[EventBus] = event_bus

    async def __call__(self, data: CreateNewChatCommand) -> CreateChatView:
        current_user: User = await self._current_user_service.get_current_user()

        logger.info(
            "Started creating new chat for user with id: %s with llm provider: %s",
            current_user.id,
            data.llm_provider
        )

        new_chat: Chat

        if data.llm_provider is None:
            logger.info("LLM provider not provided")
            new_chat = self._chat_service.create(
                user=current_user
            )
        else:
            logger.info("LLM Provider provided: %s", data.llm_provider)
            new_chat = self._chat_service.create(
                user=current_user,
                selected_llm=LLMProviderType(data.llm_provider)
            )

        logger.info("Created new chat: %s", new_chat)

        logger.info("Requesting command gateway for adding new chat in persistence storage: %s", new_chat)
        await self._chat_command_gateway.add(chat=new_chat)

        logger.info("Started publishing events from chat service")
        await self._event_bus.publish(self._chat_service.pull_events())

        logger.info("Started committing")
        await self._transaction_manager.commit()

        logger.info("Finished adding new chat, new chat id: %s", new_chat.id)

        return CreateChatView(
            chat_id=new_chat.id
        )
