from typing import Final

from sqlalchemy import Delete, delete, select, Select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from chat_service.application.common.ports.chat.chat_command_gateway import ChatCommandGateway
from chat_service.domain.chat.entities import Chat
from chat_service.domain.chat.values.chat_id import ChatID
from chat_service.infrastructure.adapters.persistence.constants import DB_QUERY_FAILED
from chat_service.infrastructure.errors.transaction_manager import RepoError
from chat_service.infrastructure.persistence.models.chat import messages_table


class SqlAlchemyChatCommandGateway(ChatCommandGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    async def add(self, chat: Chat) -> None:
        try:
            self._session.add(chat)
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error

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
    async def update(self, chat: Chat) -> None:
        # Update chat itself
        update_stmt = (
            update(Chat)
            .where(Chat.id == chat.id)  # type: ignore
            .values(
                user_id=chat.user.id,
                selected_llm=chat.selected_llm,
                updated_at=chat.updated_at,
            )
        )

        try:
            await self._session.execute(update_stmt)

            if chat.messages:
                messages_data = [
                    {
                        "id": message.id,
                        "chat_id": chat.id,
                        "content": str(message.content.value),
                        "role": message.role,
                        "status": message.status,
                        "created_at": message.created_at,
                        "updated_at": message.updated_at,
                    }
                    for message in chat.messages
                ]
                insert_messages_stmt = (
                    pg_insert(messages_table)
                    .values(messages_data)
                    .on_conflict_do_update(
                        index_elements=["id"],
                        set_={
                            "content": pg_insert(messages_table).excluded.content,
                            "role": pg_insert(messages_table).excluded.role,
                            "status": pg_insert(messages_table).excluded.status,
                            "updated_at": pg_insert(messages_table).excluded.updated_at,
                        },
                    )
                )
                await self._session.execute(insert_messages_stmt)

        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error

    @override
    async def delete_by_id(self, chat_id: ChatID) -> None:
        delete_stm: Delete = delete(Chat).where(Chat.id == chat_id)  # type: ignore

        try:
            await self._session.execute(delete_stm)
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error
