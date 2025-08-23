import os

from pydantic import BaseModel, Field

from compressor.setup.configs.broker import RabbitMQConfig
from compressor.setup.configs.cache import RedisConfig
from compressor.setup.configs.database import PostgresConfig, SQLAlchemyConfig
from compressor.setup.configs.logs import LoggingConfig
from compressor.setup.configs.task_iq import TaskIQConfig
from compressor.setup.configs.telegram import TGConfig


class AppConfig(BaseModel):
    logging: LoggingConfig = Field(
        default_factory=lambda: LoggingConfig(**os.environ),
        description="Logging config",
    )
    broker: RabbitMQConfig = Field(
        default_factory=lambda: RabbitMQConfig(**os.environ),
        description="Broker config",
    )
    cache: RedisConfig = Field(
        default_factory=lambda: RedisConfig(**os.environ),
        description="Cache config",
    )
    task_manager: TaskIQConfig = Field(
        default_factory=lambda: TaskIQConfig(**os.environ),
        description="Task manager config"
    )
    telegram_bot: TGConfig = Field(
        default_factory=lambda: TGConfig(**os.environ),
        description="Telegram bot config"
    )
    database: PostgresConfig = Field(
        default_factory=lambda: PostgresConfig(**os.environ),
        description="Database config"
    )
    alchemy: SQLAlchemyConfig = Field(
        default_factory=lambda: SQLAlchemyConfig(**os.environ),
        description="Alchemy config"
    )
