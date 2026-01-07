"""Imperative mapping for User entity."""
from typing import Final

import sqlalchemy as sa
from sqlalchemy.orm import composite

from chat_service.domain.user.entities.user import User
from chat_service.domain.user.values.user_name import UserName
from chat_service.domain.user.values.user_role import UserRole
from chat_service.infrastructure.persistence.models.base import mapper_registry

users_table: Final[sa.Table] = sa.Table(
    "users",
    mapper_registry.metadata,
    sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column("name", sa.String(255), nullable=False),
    sa.Column("role", sa.Enum(UserRole), nullable=False),
    sa.Column("is_active", sa.Boolean, nullable=False),
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


def map_users_table() -> None:
    """Map User entity to users table using imperative mapping."""
    mapper_registry.map_imperatively(
        User,
        users_table,
        properties={
            "id": users_table.c.id,
            "name": composite(UserName, users_table.c.name),
            "role": users_table.c.role,
            "is_active": users_table.c.is_active,
            "created_at": users_table.c.created_at,
            "updated_at": users_table.c.updated_at,
        },
        column_prefix="_",
    )
