from typing import Final

import sqlalchemy as sa
from sqlalchemy.orm import composite, relationship

from compressor.domain.users.entities.telegram_user import TelegramUser
from compressor.domain.users.values.user_first_name import UserFirstName
from compressor.infrastructure.persistence.models.base import mapper_registry

telegram_users_table: Final[sa.Table] = sa.Table(
    "telegram_users",
    mapper_registry.metadata,
    sa.Column("telegram_id", sa.BigInteger, primary_key=True),
    sa.Column(
        "user_id", sa.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=True
    ),
    sa.Column("first_name", sa.String(255), nullable=False),
    sa.Column("username", sa.String(255), nullable=True),
    sa.Column("last_name", sa.String(255), nullable=True),
    sa.Column("is_premium", sa.Boolean, nullable=False, default=False),
    sa.Column("is_bot", sa.Boolean, nullable=False, default=False),
    sa.Column(
        "created_at",
        sa.DateTime,
        default=sa.func.now(),
        server_default=sa.func.now(),
        nullable=False,
    ),
    sa.Column(
        "updated_at",
        sa.DateTime,
        default=sa.func.now(),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        server_onupdate=sa.func.now(),
        nullable=True,
    ),
)


def map_telegram_user_table() -> None:
    mapper_registry.map_imperatively(
        TelegramUser,
        telegram_users_table,
        properties={
            "id": telegram_users_table.c.telegram_id,
            "first_name": composite(UserFirstName, telegram_users_table.c.first_name),
            "user": relationship("User", back_populates="telegram", uselist=False),
        },
        column_prefix="_",
    )
