from typing import Final

import sqlalchemy as sa
from sqlalchemy import join, Join
from sqlalchemy.orm import composite, relationship

from cryptography_methods.infrastructure.persistence.models.base import mapper_registry

users_table: Final[sa.Table] = sa.Table(
    "users",
    mapper_registry.metadata,
    sa.Column("id", sa.UUID, primary_key=True),
    sa.Column("first_name", sa.String(255), nullable=False),
    sa.Column("role_id", sa.ForeignKey("roles.id"), nullable=False),
    sa.Column("telegram_account_id", sa.ForeignKey("telegram_accounts.telegram_id"), nullable=True),
    sa.Column("is_blocked", sa.Boolean, default=False, server_default="false"),
    sa.Column("middle_name", sa.String(255), nullable=True),
    sa.Column("second_name", sa.String(255), nullable=True),
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

telegram_accounts_table: Final[sa.Table] = sa.Table(
    "telegram_accounts",
    mapper_registry.metadata,
    sa.Column("telegram_id", sa.Integer, nullable=False, primary_key=True),
    sa.Column("is_bot", sa.Boolean, default=False, nullable=True),
    sa.Column("language_code", sa.String(5), nullable=True),
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

roles_table: Final[sa.Table] = sa.Table(
    "roles",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(25), nullable=False, unique=True),
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


def map_user_aggregate() -> None:
    from cryptography_methods.domain.user.entities.user import User
    from cryptography_methods.domain.user.values.first_name import FirstName
    from cryptography_methods.domain.user.values.second_name import SecondName
    from cryptography_methods.domain.common.values import CreateTime, UpdateTime
    from cryptography_methods.domain.user.entities.telegram import TelegramAccount
    from cryptography_methods.domain.user.values.middle_name import MiddleName
    from cryptography_methods.domain.user.values.user_role import UserRole

    mapper_registry.map_imperatively(
        TelegramAccount,
        telegram_accounts_table,
        properties={
            "users": relationship(User),
            "telegram_id": telegram_accounts_table.c.id,
            "is_bot": telegram_accounts_table.c.is_bot,
            "language_code": telegram_accounts_table.c.language_code,
        }
    )

    mapper_registry.map_imperatively(
        UserRole,
        roles_table,
    )

    users_query_with_roles: Join = join(users_table, roles_table)
    users_query_with_telegram: Join = join(telegram_accounts_table, users_query_with_roles)

    mapper_registry.map_imperatively(
        User,
        users_query_with_telegram,
        properties={
            "id": users_table.c.user_id,
            "first_name": composite(FirstName, users_table.c.user_first_name),
            "second_name": composite(SecondName, users_table.c.user_second_name),
            "middle_name": composite(MiddleName, users_table.c.user_middle_name),
            "role": relationship(UserRole),
            "is_blocked": users_table.c.user_is_blocked,
            "telegram_account": relationship(TelegramAccount),
            "created_at": composite(CreateTime, users_table.c.users_created_at),
            "updated_at": composite(UpdateTime, users_table.c.users_updated_at)
        }
    )
