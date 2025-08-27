from typing import Final

import sqlalchemy as sa
from sqlalchemy.orm import composite, relationship

from compressor.domain.users.entities.user import User
from compressor.domain.users.values.language_code import LanguageCode
from compressor.domain.users.values.user_password_hash import UserPasswordHash
from compressor.domain.users.values.user_role import UserRole
from compressor.domain.users.values.username import Username
from compressor.infrastructure.persistence.models.base import mapper_registry

users_table: Final[sa.Table] = sa.Table(
    "users",
    mapper_registry.metadata,
    sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, unique=True, nullable=False),
    sa.Column("username", sa.String(50), nullable=False, unique=True),
    sa.Column("password_hash", sa.LargeBinary, nullable=False),
    sa.Column("role", sa.Enum(UserRole, name="userrole"), default=UserRole.USER, nullable=False),
    sa.Column("is_active", sa.Boolean, nullable=False, default=True),
    sa.Column("language_code", sa.Enum(LanguageCode, name="userlanguage"), nullable=False, default=LanguageCode.RU),
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
    mapper_registry.map_imperatively(
        User,
        users_table,
        properties={
            "id": users_table.c.id,
            "username": composite(Username, users_table.c.username),
            "password_hash": composite(UserPasswordHash, users_table.c.password_hash),
            "role": users_table.c.role,
            "language": users_table.c.language_code,
            "telegram": relationship(
                "TelegramUser", back_populates="user", uselist=False, cascade="all, delete-orphan", lazy="joined"
            ),
            "is_active": users_table.c.is_active,
        },
        column_prefix="_",
    )
