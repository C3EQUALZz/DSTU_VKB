from abc import ABC
from functools import lru_cache
from pathlib import Path

from pydantic import Field, RedisDsn, field_validator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class CommonSettings(BaseSettings, ABC):
    """
    Base class for each setting. If you add new technologies, please add new class and inherit from BaseSettings.
    """

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class RedisSettings(CommonSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT_NETWORK")
    password: str = Field(alias="REDIS_PASSWORD")

    @property
    def url(self) -> RedisDsn:
        return RedisDsn(f"redis://:{self.password}@{self.host}:{self.port}")


class ModelsSettings(CommonSettings):
    path_to_colorization_model: Path = Field(alias="PATH_TO_COLORIZATION_MODEL")

    @field_validator("path_to_colorization_model", mode="before")
    def validating_path_to_colorization_model(cls, v: str) -> Path:
        converted_to_path: Path = Path.cwd().parent.parent / Path(v)

        if not converted_to_path.exists():
            raise ValueError(f"Path {v} doesn't exists")

        return converted_to_path


class BrokerSettings(CommonSettings):
    host: str = Field(alias="BROKER_HOST")
    port: int = Field(alias="BROKER_PORT_NETWORK")

    image_color_to_grayscale_topic: str = Field(
        default="image-color-to-grayscale",
        alias="BROKER_IMAGE_COLOR_TO_GRAYSCALE"
    )

    image_grayscale_to_color_topic: str = Field(
        default="image-grayscale-to-color",
        alias="BROKER_IMAGE_GRAYSCALE_TO_COLOR"
    )

    image_crop_topic: str = Field(
        default="image-crop",
        alias="BROKER_IMAGE_CROP"
    )

    image_rotate_topic: str = Field(
        default="image-rotate",
        alias="BROKER_IMAGE_ROTATE"
    )

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class Settings(CommonSettings):
    """
    Settings class which encapsulates logic of settings from other classes.
    In application, you must use this class.
    """

    cache: RedisSettings = RedisSettings()
    models: ModelsSettings = ModelsSettings()
    broker: BrokerSettings = BrokerSettings()


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()
