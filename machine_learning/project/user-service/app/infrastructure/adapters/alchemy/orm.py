from sqlalchemy import Column, ForeignKey, String, MetaData, Table, DateTime, Boolean, Integer
from sqlalchemy.orm import relationship, registry
from sqlalchemy.sql import func

from app.infrastructure.adapters.alchemy.type_decorators import (
    TextModelDecorator,
    ImageModelDecorator,
    RoleDecorator,
    PositiveNumberDecorator,
    StringUUID, EmailTypeDecorator, PasswordTypeDecorator,
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
    Column("telegram_id", Integer, nullable=True),
    Column("is_verified", Boolean, nullable=False),
    Column("created_at", DateTime(timezone=True), default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
    ),
)

settings_table = Table(
    "settings",
    metadata,
    Column("oid", StringUUID(), primary_key=True),
    Column(
        "user_id",
        StringUUID(),
        ForeignKey("users.oid", ondelete="CASCADE"),
        unique=True
    ),
    Column("text_model", TextModelDecorator(50), nullable=False),
    Column("image_model", ImageModelDecorator(50), nullable=False),
    Column("created_at", DateTime(timezone=True), default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
    ),
)

statistics_table = Table(
    "statistics",
    metadata,
    Column("oid", StringUUID(), primary_key=True),
    Column(
        "user_id",
        StringUUID(),
        ForeignKey("users.oid", ondelete="CASCADE"),
        unique=True
    ),
    Column("text_requests", PositiveNumberDecorator(), default=0),
    Column("image_requests", PositiveNumberDecorator(), default=0),
    Column("voice_requests", PositiveNumberDecorator(), default=0),
    Column("created_at", DateTime(timezone=True), default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
    ),
)

personal_chats_table = Table(
    "personal_chats",
    metadata,
    Column("oid", StringUUID(), primary_key=True),
    Column("user_id", StringUUID(), ForeignKey("users.oid"), unique=True),
    Column("settings_id", StringUUID(), ForeignKey("settings.oid")),
    Column("statistics_id", StringUUID(), ForeignKey("statistics.oid")),
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
    from app.domain.entities.settings import SettingsEntity
    from app.domain.entities.statistic import StatisticsEntity
    from app.domain.entities.chat import PersonalChatEntity

    # User
    mapper_registry.map_imperatively(
        UserEntity,
        users_table,
        properties={
            "settings": relationship(
                SettingsEntity,
                uselist=False,
                back_populates="user"
            ),
            "statistics": relationship(
                StatisticsEntity,
                uselist=False,
                back_populates="user"
            ),
            "chat": relationship(
                PersonalChatEntity,
                uselist=False,
                back_populates="user"
            ),
        }
    )

    # Settings
    mapper_registry.map_imperatively(
        SettingsEntity,
        settings_table,
        properties={
            "user": relationship(
                UserEntity,
                back_populates="settings"
            ),
        }
    )

    # Statistics
    mapper_registry.map_imperatively(
        StatisticsEntity,
        statistics_table,
        properties={
            "user": relationship(
                UserEntity,
                back_populates="statistics"
            ),
        }
    )

    # Personal Chat
    mapper_registry.map_imperatively(
        PersonalChatEntity,
        personal_chats_table,
        properties={
            "user": relationship(
                UserEntity,
                back_populates="chat"
            ),
            "settings": relationship(SettingsEntity),
            "statistics": relationship(StatisticsEntity),
        }
    )
