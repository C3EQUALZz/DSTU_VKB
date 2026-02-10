import os

from pydantic import BaseModel, Field

from fulla.setup.configs.logging import LoggingConfig
from fulla.setup.configs.training import TrainingConfig


class ApplicationConfig(BaseModel):

    logging: LoggingConfig = Field(
        default_factory=lambda: LoggingConfig(**os.environ),
        description="Logging settings",
    )

    training: TrainingConfig = Field(
        default_factory=TrainingConfig,
        description="Training experiment settings",
    )
