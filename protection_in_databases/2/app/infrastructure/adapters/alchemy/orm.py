from sqlalchemy import Column, String, MetaData, Table, DateTime, Boolean
from sqlalchemy.orm import registry
from sqlalchemy.sql import func

from app.infrastructure.adapters.alchemy.type_decorators import (
    RoleDecorator,
    StringUUID,
    EmailTypeDecorator,
    PasswordTypeDecorator,
)

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

# Таблицы
users_table = Table(
    "users",
    metadata,
    Column("oid", StringUUID(), primary_key=True),
    Column("name", String(100), nullable=False),
    Column("surname", String(100), nullable=False),
    Column("email", EmailTypeDecorator(100), nullable=False),
    Column("password", PasswordTypeDecorator(100), nullable=False),
    Column("role", RoleDecorator(20), nullable=False),
    Column("is_verified", Boolean, nullable=False),
    Column("created_at", DateTime(timezone=True), default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
    ),
)


# Маппинг
def start_mappers() -> None:
    from app.domain.entities.user import UserEntity

    # User
    mapper_registry.map_imperatively(
        UserEntity,
        users_table,
    )
