from typing import Final

import sqlalchemy as sa
from sqlalchemy.orm import composite, relationship

from compressor.infrastructure.persistence.models.base import mapper_registry

users_table: Final[sa.Table] = sa.Table(
    "users",
    mapper_registry.metadata,
    sa.Column("user_id", sa.UUID, primary_key=True, unique=True, nullable=False),
    sa.Column("username", sa.String(50), nullable=False, unique=True),
    sa.Column("password_hash", sa.BINARY(255), nullable=False),
    sa.Column("role", sa.String(50), nullable=False),
    sa.Column("is_active", sa.Boolean, nullable=False, default=True),
    sa.Column("language_code", sa.String(10), nullable=False, default="ru"),
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


def map_user_table() -> None:
    from compressor.domain.users.entities.user import User
    from compressor.domain.users.values.user_id import UserID
    from compressor.domain.users.values.username import Username
    from compressor.domain.users.values.user_password_hash import UserPasswordHash
    from compressor.domain.users.values.user_role import UserRole
    from compressor.domain.users.values.language_code import LanguageCode

    mapper_registry.map_imperatively(
        User,
        users_table,
        properties={
            "id": composite(UserID, users_table.c.user_id),
            "username": composite(Username, users_table.c.username),
            "password_hash": composite(UserPasswordHash, users_table.c.password_hash),
            "role": composite(UserRole, users_table.c.role),
            "language": composite(LanguageCode, users_table.c.language_code),
            "telegram": relationship(
                "TelegramUser",
                back_populates="user",
                uselist=False,
                cascade="all, delete-orphan",
                lazy="joined"
            ),
        },
    )
