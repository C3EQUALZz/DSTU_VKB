import os

from pydantic import BaseModel, Field

from compressor.setup.configs.broker import RabbitMQConfig
from compressor.setup.configs.cache import RedisConfig
from compressor.setup.configs.logs import LoggingConfig


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
