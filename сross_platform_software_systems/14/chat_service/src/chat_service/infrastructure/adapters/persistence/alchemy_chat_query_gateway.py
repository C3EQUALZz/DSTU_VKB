from typing import Final

from sqlalchemy import select, Select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from chat_service.application.common.ports.chat.chat_query_gateway import ChatQueryGateway
from chat_service.domain.chat.entities import Chat
from chat_service.domain.chat.values.chat_id import ChatID
from chat_service.infrastructure.adapters.persistence.constants import DB_QUERY_FAILED
from chat_service.infrastructure.errors.transaction_manager import RepoError


class SqlAlchemyChatQueryGateway(ChatQueryGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    async def read_by_id(self, chat_id: ChatID) -> Chat | None:
        select_stmt: Select[tuple[Chat]] = select(Chat).where(Chat.id == chat_id)  # type: ignore

        try:
            chat: Chat | None = (await self._session.execute(select_stmt)).scalar_one_or_none()
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error
        else:
            return chat

    @override
    async def read_all(self) -> list[Chat] | None:
        ...
