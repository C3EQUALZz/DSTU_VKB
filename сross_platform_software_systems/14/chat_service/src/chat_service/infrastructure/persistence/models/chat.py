"""Imperative mapping for Chat and Message entities."""
import sqlalchemy as sa
from sqlalchemy.orm import composite, relationship
from typing import Final

from chat_service.domain.chat.entities.chat import Chat
from chat_service.domain.chat.entities.message import Message
from chat_service.domain.chat.values.llm_provider import LLMProviderType
from chat_service.domain.chat.values.message_content import MessageContent
from chat_service.domain.chat.values.message_role import MessageRole
from chat_service.domain.chat.values.message_status import MessageStatus
from chat_service.infrastructure.persistence.models.base import mapper_registry

chats_table: Final[sa.Table] = sa.Table(
    "chats",
    mapper_registry.metadata,
    sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column("user_id", sa.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
    sa.Column("selected_llm", sa.Enum(LLMProviderType), nullable=False),
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        default=sa.func.now(),
        server_default=sa.func.now(),
        nullable=False,
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        default=sa.func.now(),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=True,
    ),
)

messages_table: Final[sa.Table] = sa.Table(
    "messages",
    mapper_registry.metadata,
    sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column("chat_id", sa.UUID(as_uuid=True), sa.ForeignKey("chats.id"), nullable=False),
    sa.Column("content", sa.Text, nullable=False),
    sa.Column("role", sa.Enum(MessageRole), nullable=False),
    sa.Column("status", sa.Enum(MessageStatus), nullable=False),
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        default=sa.func.now(),
        server_default=sa.func.now(),
        nullable=False,
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        default=sa.func.now(),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=True,
    ),
)


def map_chats_table() -> None:
    """Map Chat entity to chats table using imperative mapping."""
    mapper_registry.map_imperatively(
        Chat,
        chats_table,
        properties={
            "id": chats_table.c.id,
            "user": relationship(
                "User",
                lazy="select",
            ),
            "selected_llm": chats_table.c.selected_llm,
            "messages": relationship(
                "Message",
                back_populates="_chat",
                lazy="select",
                order_by=messages_table.c.created_at,
            ),
            "created_at": chats_table.c.created_at,
            "updated_at": chats_table.c.updated_at,
        },
        column_prefix="_",
    )


def map_messages_table() -> None:
    """Map Message entity to messages table using imperative mapping."""
    mapper_registry.map_imperatively(
        Message,
        messages_table,
        properties={
            "id": messages_table.c.id,
            "content": composite(MessageContent, messages_table.c.content),
            "role": messages_table.c.role,
            "status": messages_table.c.status,
            "_chat": relationship(
                "Chat",
                back_populates="messages",
            ),
            "created_at": messages_table.c.created_at,
            "updated_at": messages_table.c.updated_at,
        },
        column_prefix="_",
    )
