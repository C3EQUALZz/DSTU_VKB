from taskiq import AsyncBroker

from compressor.setup.bootstrap import setup_task_manager
from compressor.setup.configs.settings import AppConfig


def create_taskiq_app() -> AsyncBroker:
    config: AppConfig = AppConfig()
    task_manager: AsyncBroker = setup_task_manager(
        taskiq_config=config.task_manager,
        rabbitmq_config=config.broker,
        redis_config=config.cache
    )
    return task_manager
