import logging
from dataclasses import dataclass
from typing import final, Final
from uuid import UUID

from chat_service.application.common.ports.chat.chat_query_gateway import ChatQueryGateway
from chat_service.application.common.services.current_user_service import CurrentUserService
from chat_service.domain.chat.services.chat_service import ChatService
from chat_service.domain.chat.services.message_service import MessageService
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
            chat_service: ChatService,
            message_service: MessageService,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._chat_query_gateway: Final[ChatQueryGateway] = chat_query_gateway
        self._chat_service: Final[ChatService] = chat_service
        self._message_service: Final[MessageService] = message_service

    async def __call__(self, data: RequestOnUserMessageInChatCommand):
        current_user: User = await self._current_user_service.get_current_user()


