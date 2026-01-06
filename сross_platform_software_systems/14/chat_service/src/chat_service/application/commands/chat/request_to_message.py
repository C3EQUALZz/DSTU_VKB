import logging
from dataclasses import dataclass
from typing import final, Final
from uuid import UUID

from chat_service.application.common.ports.chat.chat_query_gateway import ChatQueryGateway
from chat_service.application.common.services.current_user_service import CurrentUserService

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
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._chat_query_gateway: Final[ChatQueryGateway] = chat_query_gateway

    async def __call__(self, data: RequestOnUserMessageInChatCommand):
        ...
