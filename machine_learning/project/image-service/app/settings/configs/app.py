import multiprocessing
import pathlib
from abc import ABC
from functools import lru_cache
from pathlib import Path
from typing import Optional, Literal

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
    path_to_stylization_model: Path = Field(alias="PATH_TO_STYLIZATION_MODEL")

    @field_validator("path_to_stylization_model", mode="before")
    def validating_path_to_stylization_model(cls, v: str) -> Path:
        converted_to_path: Path = Path.cwd().parent.parent / Path(v)

        if not converted_to_path.exists():
            raise ValueError(f"Path {v} doesn't exists")

        return converted_to_path

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

    image_color_to_grayscale_result_topic: str = Field(
        default="image-color-to-grayscale-result",
        alias="BROKER_IMAGE_COLOR_TO_GRAYSCALE"
    )

    image_color_to_grayscale_group: str = Field(
        default="image-color-to-grayscale-group",
        alias="BROKER_IMAGE_COLOR_TO_GRAYSCALE_GROUP"
    )

    image_grayscale_to_color_topic: str = Field(
        default="image-grayscale-to-color",
        alias="BROKER_IMAGE_GRAYSCALE_TO_COLOR"
    )

    image_grayscale_to_color_result_topic: str = Field(
        default="image-grayscale-to-color-result",
        alias="BROKER_IMAGE_GRAYSCALE_TO_COLOR"
    )

    image_grayscale_to_color_group: str = Field(
        default="image-grayscale-to-color-group",
        alias="BROKER_IMAGE_GRAYSCALE_TO_COLOR_GROUP"
    )

    image_crop_topic: str = Field(
        default="image-crop",
        alias="BROKER_IMAGE_CROP"
    )

    image_crop_result_topic: str = Field(
        default="image-crop-result",
        alias="BROKER_IMAGE_CROP_RESULT"
    )

    image_crop_group: str = Field(
        default="image-crop-group",
        alias="BROKER_IMAGE_CROP_GROUP"
    )

    image_rotate_topic: str = Field(
        default="image-rotate",
        alias="BROKER_IMAGE_ROTATE"
    )

    image_rotate_result_topic: str = Field(
        default="image-rotate-result",
        alias="BROKER_IMAGE_ROTATE_RESULT"
    )

    image_rotate_group: str = Field(
        default="image-rotate-group",
        alias="BROKER_IMAGE_ROTATE_GROUP"
    )

    image_style_topic: str = Field(
        default="image-style",
        alias="BROKER_IMAGE_STYLE"
    )

    image_style_result_topic: str = Field(
        default="image-style-result",
        alias="BROKER_IMAGE_STYLE_RESULT"
    )

    image_style_group: str = Field(
        default="image-style-group",
        alias="BROKER_IMAGE_STYLE_GROUP"
    )

    image_inverse_topic: str = Field(
        default="image-inverse",
        alias="BROKER_IMAGE_INVERSE"
    )

    image_inverse_result_topic: str = Field(
        default="image-inverse-result",
        alias="BROKER_IMAGE_INVERSE_RESULT"
    )

    image_inverse_group: str = Field(
        default="image-inverse-group",
        alias="BROKER_IMAGE_INVERSE_GROUP"
    )

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class SchedulerSettings(CommonSettings):
    host: str = Field(alias="WORKER_HOST")
    port: int = Field(alias="WORKER_PORT")


class ServerSettings(CommonSettings):
    multiprocess_dir: Optional[Path] = Field(alias="PROMETHEUS_MULTIPROC_DIR", default=None)
    workers: int = Field(alias="SERVER_WORKERS", default=multiprocessing.cpu_count() * 2 + 1)
    max_requests: int = Field(alias="SERVER_MAX_REQUESTS", default=1000)
    max_jitter: int = Field(alias="SERVER_MAX_JITTER", default=50)
    bind: str = Field(alias="SERVER_BIND")
    timeout: int = Field(alias="SERVER_TIMEOUT")
    worker_class: str = Field(alias="SERVER_WORKER_CLASS")
    log_level: str = Field(alias="SERVER_LOG_LEVEL")
    log_file: str = Field(alias="SERVER_LOG_FILE")


class CORSSettings(CommonSettings):
    allow_origins: list[str] = Field(alias="CORS_ALLOW_ORIGINS")
    allow_headers: list[str] = Field(alias="CORS_ALLOW_HEADERS")
    allow_credentials: bool = Field(alias="CORS_ALLOW_CREDENTIALS")
    allow_methods: list[str] = Field(alias="CORS_ALLOW_METHODS")


class SentrySettings(CommonSettings):
    dsn: str = Field(alias="SENTRY_DSN")
    send_default_pii: bool = Field(alias="SENTRY_SEND_DEFAULT_PII", default=True)
    traces_sample_rate: float = Field(alias="SENTRY_TRACES_SAMPLE_RATE", default=1.0)
    profile_session_sample_rate: float = Field(alias="SENTRY_PROFILE_SESSION_SAMPLE_RATE", default=1.0)
    profile_lifecycle: Literal["manual", "trace"] = Field(alias="SENTRY_PROFILE_LIFECYCLE", default="trace")


class Settings(CommonSettings):
    """
    Settings class which encapsulates logic of settings from other classes.
    In application, you must use this class.
    """

    cache: RedisSettings = RedisSettings()
    models: ModelsSettings = ModelsSettings()
    broker: BrokerSettings = BrokerSettings()
    scheduler: SchedulerSettings = SchedulerSettings()
    cors: CORSSettings = CORSSettings()
    server: ServerSettings = ServerSettings()
    sentry: SentrySettings = SentrySettings()
    project_dir: Path = pathlib.Path(__file__).parent.parent.parent.parent


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()
