import logging
from dataclasses import dataclass
from typing import final, Final
from uuid import UUID

from chat_service.application.common.ports.chat.chat_command_gateway import ChatCommandGateway
from chat_service.application.common.ports.chat.chat_query_gateway import ChatQueryGateway
from chat_service.application.common.ports.chat.openrouter_gateway import OpenRouterGateway, ChatCompletionDTO
from chat_service.application.common.ports.transaction_manager import TransactionManager
from chat_service.application.common.services.current_user_service import CurrentUserService
from chat_service.application.common.views.chat.request_on_user_message import RequestOnUserMessageView
from chat_service.application.errors.chat import ChatNotFoundError
from chat_service.domain.chat.entities import Chat, Message
from chat_service.domain.chat.services.chat_service import ChatService
from chat_service.domain.chat.services.message_service import MessageService
from chat_service.domain.chat.values.chat_id import ChatID
from chat_service.domain.chat.values.message_content import MessageContent
from chat_service.domain.chat.values.message_role import MessageRole
from chat_service.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class RequestOnUserMessageInChatCommand:
    content: str
    chat_id: UUID


@final
class RequestOnUserMessageInChatCommandHandler:
    def __init__(
            self,
            current_user_service: CurrentUserService,
            chat_query_gateway: ChatQueryGateway,
            chat_command_gateway: ChatCommandGateway,
            chat_service: ChatService,
            message_service: MessageService,
            transaction_manager: TransactionManager,
            openrouter_gateway: OpenRouterGateway,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._chat_query_gateway: Final[ChatQueryGateway] = chat_query_gateway
        self._chat_service: Final[ChatService] = chat_service
        self._message_service: Final[MessageService] = message_service
        self._chat_command_gateway: Final[ChatCommandGateway] = chat_command_gateway
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._open_router_gateway: Final[OpenRouterGateway] = openrouter_gateway

    async def __call__(self, data: RequestOnUserMessageInChatCommand) -> RequestOnUserMessageView:
        current_user: User = await self._current_user_service.get_current_user()

        chat_id: ChatID = ChatID(data.chat_id)
        message_content: MessageContent = MessageContent(data.content)

        existing_chat: Chat | None = await self._chat_query_gateway.read_by_id(
            chat_id=chat_id,
        )

        if existing_chat is None:
            msg = f"Chat with id {data.chat_id} not found"
            raise ChatNotFoundError(msg)

        new_message: Message = self._message_service.create(
            content=message_content,
            role=MessageRole.USER,
        )

        self._chat_service.add_message(chat=existing_chat, message=new_message)

        request_from_llm: ChatCompletionDTO = await self._open_router_gateway.send_message_to_chat(
            chat=existing_chat
        )

        llm_message_content: MessageContent = MessageContent(request_from_llm.content)

        converted_message_from_llm: Message = self._message_service.create(
            content=llm_message_content,
            role=MessageRole.ASSISTANT,
        )

        self._chat_service.add_message(
            chat=existing_chat,
            message=converted_message_from_llm
        )

        await self._chat_command_gateway.update(chat=existing_chat)
        await self._transaction_manager.commit()

        return RequestOnUserMessageView(
            user_message_id=new_message.id,
            assistant_message_id=converted_message_from_llm.id,
            assistant_message_content=converted_message_from_llm.content.value,
        )
