import os

from pydantic import BaseModel, Field

from fulla.setup.configs.logging import LoggingConfig


class ApplicationConfig(BaseModel):

    logging: LoggingConfig = Field(
        default_factory=lambda: LoggingConfig(**os.environ),
        description="Logging settings",
    )
