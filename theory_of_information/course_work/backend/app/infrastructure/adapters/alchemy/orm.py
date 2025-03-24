from sqlalchemy import Table, Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.infrastructure.adapters.alchemy.metadata import metadata, mapper_registry
from app.infrastructure.adapters.alchemy.type_decorators import PhoneNumberTypeDecorator, EmailTypeDecorator, \
    PasswordTypeDecorator, GenderTypeDecorator, URLTypeDecorator, StatusDecorator, RoleDecorator

users_table = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, key="oid"),
    Column("surname", String(100)),
    Column("name", String(100), nullable=False),
    Column("patronymic", String(100)),
    Column("email", EmailTypeDecorator(100), nullable=False, unique=True),
    Column("password", PasswordTypeDecorator(50), nullable=False),
    Column("role", RoleDecorator(15), nullable=False),
    Column("status", StatusDecorator(10), nullable=False),
    Column("created_at", DateTime(timezone=True), default=func.now()),
    Column("updated_at", DateTime(timezone=True), default=func.now(), onupdate=func.now()),
)

bios_table = Table(
    "bios",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, key="oid"),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.oid", onupdate='CASCADE', ondelete='CASCADE'), unique=True),
    Column("phone_number", PhoneNumberTypeDecorator(16)),
    Column("photo", URLTypeDecorator(255)),
    Column("gender", GenderTypeDecorator(10)),
    Column("created_at", DateTime(timezone=True), default=func.now()),
    Column("updated_at", DateTime(timezone=True), default=func.now(), onupdate=func.now()),
)

addresses_table = Table(
    "addresses",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, key="oid"),
    Column("bio_id", UUID(as_uuid=True), ForeignKey("bios.oid", onupdate='CASCADE', ondelete='CASCADE')),
    Column("country", String(100)),
    Column("city", String(100)),
    Column("street", String(100)),
    Column("postal_code", String(20)),
    Column("created_at", DateTime(timezone=True), default=func.now()),
    Column("updated_at", DateTime(timezone=True), default=func.now(), onupdate=func.now())
)

social_networks_table = Table(
    "social_networks",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, key="oid"),
    Column("bio_id", UUID(as_uuid=True), ForeignKey("bios.oid", onupdate='CASCADE', ondelete='CASCADE')),
    Column("platform_id", UUID(as_uuid=True), ForeignKey("platforms.id"), nullable=False),
    Column("url", String(255), nullable=False),
    Column("created_at", DateTime(timezone=True), default=func.now()),
    Column("updated_at", DateTime(timezone=True), default=func.now(), onupdate=func.now())
)

platforms_table = Table(
    "platforms",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String(50), nullable=False, unique=True)
)


def start_mappers() -> None:
    """
    Map all domain models to ORM models, for purpose of using domain models directly during work with the database,
    according to DDD.
    """
    from app.domain.entities.user import UserEntity
    from app.domain.entities.bio import BioEntity
    from app.domain.entities.address import AddressEntity
    from app.domain.entities.social_network import SocialNetworkEntity
    from app.domain.values.social_network import Platform

    mapper_registry.map_imperatively(
        class_=AddressEntity,
        local_table=addresses_table,
        properties={
            "oid": addresses_table.c.oid
        }
    )

    mapper_registry.map_imperatively(
        class_=UserEntity,
        local_table=users_table,
        properties={
            "oid": users_table.c.oid,
        }
    )

    mapper_registry.map_imperatively(
        class_=SocialNetworkEntity,
        local_table=social_networks_table,
        properties={
            "bio": relationship(BioEntity, back_populates="social_networks"),
            "oid": social_networks_table.c.oid
        }
    )

    mapper_registry.map_imperatively(
        class_=BioEntity,
        local_table=bios_table,
        properties={
            "social_networks": relationship(SocialNetworkEntity, back_populates="bio", cascade="all, delete-orphan"),
            "oid": bios_table.c.oid
        }
    )

    mapper_registry.map_imperatively(
        class_=Platform,
        local_table=platforms_table,
        properties={
            "value": platforms_table.c.name,
        }
    )
