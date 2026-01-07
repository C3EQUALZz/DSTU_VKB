import os
from pydantic import BaseModel, Field

from chat_service.setup.config.asgi import ASGIConfig
from chat_service.setup.config.database import PostgresConfig, SQLAlchemyConfig
from chat_service.setup.config.openrouter import OpenRouterConfig
from chat_service.setup.config.rabbit import RabbitConfig


class AppConfig(BaseModel):
    # load_dotenv(r"D:\PycharmProjects\PixErase\backend\.env")

    postgres: PostgresConfig = Field(
        default_factory=lambda: PostgresConfig(**os.environ),
        description="Postgres settings",
    )
    alchemy: SQLAlchemyConfig = Field(
        default_factory=lambda: SQLAlchemyConfig(**os.environ),
        description="SQLAlchemy settings",
    )
    rabbitmq: RabbitConfig = Field(
        default_factory=lambda: RabbitConfig(**os.environ),
        description="RabbitMQ settings",
    )
    asgi: ASGIConfig = Field(
        default_factory=lambda: ASGIConfig(**os.environ),
        description="ASGI settings",
    )
    openrouter: OpenRouterConfig = Field(
        default_factory=lambda: OpenRouterConfig(**os.environ),
        description="OpenRouter settings",
    )
