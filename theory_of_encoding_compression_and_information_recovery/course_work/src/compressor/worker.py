from dishka import AsyncContainer, make_async_container
from dishka.integrations.taskiq import setup_dishka
from taskiq import AsyncBroker

from compressor.infrastructure.adapters.common.password_hasher_bcrypt import PasswordPepper
from compressor.setup.bootstrap import setup_task_manager
from compressor.setup.configs.cache import RedisConfig
from compressor.setup.configs.database import PostgresConfig, SQLAlchemyConfig
from compressor.setup.configs.s3 import S3Config
from compressor.setup.configs.settings import AppConfig
from compressor.setup.configs.telegram import TGConfig
from compressor.setup.ioc import setup_providers


def create_taskiq_app() -> AsyncBroker:
    config: AppConfig = AppConfig()
    task_manager: AsyncBroker = setup_task_manager(
        taskiq_config=config.task_manager,
        rabbitmq_config=config.broker,
        redis_config=config.cache
    )

    context = {
        RedisConfig: config.cache,
        PostgresConfig: config.database,
        SQLAlchemyConfig: config.alchemy,
        S3Config: config.s3,
        PasswordPepper: config.telegram_bot.pepper,
        TGConfig: config.telegram_bot
    }

    container: AsyncContainer = make_async_container(*setup_providers(), context=context)

    setup_dishka(container, broker=task_manager)

    return task_manager
