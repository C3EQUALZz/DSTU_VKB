from abc import ABC
from functools import lru_cache
from pathlib import Path

from pydantic import (
    Field,
    RedisDsn,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class CommonSettings(BaseSettings, ABC):
    """
    Base class for each setting. If you add new technologies, please add new class and inherit from BaseSettings.
    """

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class TelegramSettings(CommonSettings):
    """
    Telegram settings. Here you provide settings from .env to connect to telegram.
    """

    token: str = Field(alias="TELEGRAM_TOKEN")


class RedisSettings(CommonSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT_NETWORK")
    password: str = Field(alias="REDIS_PASSWORD")

    @property
    def url(self) -> RedisDsn:
        return RedisDsn(f"redis://:{self.password}@{self.host}:{self.port}")


class HTTPXSettings(CommonSettings):
    user_microservice_url: str = Field(alias="USER_MICROSERVICE_URL")


class BrokerSettings(CommonSettings):
    host: str = Field(alias="BROKER_HOST")
    port: int = Field(alias="BROKER_PORT_NETWORK")

    image_color_to_grayscale_topic: str = Field(
        default="image-color-to-grayscale",
        alias="BROKER_IMAGE_COLOR_TO_GRAYSCALE"
    )

    image_color_to_grayscale_result_topic: str = Field(
        default="image-color-to-grayscale-result",
        alias="BROKER_IMAGE_COLOR_TO_GRAYSCALE_RESULT"
    )

    image_grayscale_to_color_topic: str = Field(
        default="image-grayscale-to-color",
        alias="BROKER_IMAGE_GRAYSCALE_TO_COLOR"
    )

    image_grayscale_to_color_result_topic: str = Field(
        default="image-grayscale-to-color-result",
        alias="BROKER_IMAGE_GRAYSCALE_TO_COLOR_RESULT"
    )

    image_crop_topic: str = Field(
        default="image-crop",
        alias="BROKER_IMAGE_CROP_TOPIC"
    )

    image_crop_result_topic: str = Field(
        default="image-crop-result",
        alias="BROKER_IMAGE_CROP_RESULT"
    )

    image_rotate_topic: str = Field(
        default="image-rotate",
        alias="BROKER_IMAGE_ROTATE"
    )

    image_rotate_result_topic: str = Field(
        default="image-rotate-result",
        alias="BROKER_IMAGE_ROTATE_RESULT"
    )

    image_style_topic: str = Field(
        default="image-style",
        alias="BROKER_IMAGE_STYLE"
    )

    image_style_result_topic: str = Field(
        default="image-style-result",
        alias="BROKER_IMAGE_STYLE_RESULT"
    )

    image_metadata_topic: str = Field(
        default="image-metadata",
        alias="BROKER_IMAGE_METADATA"
    )

    image_metadata_result_topic: str = Field(
        default="image-metadata-result",
        alias="BROKER_IMAGE_METADATA_RESULT"
    )

    image_telegram_group: str = Field(
        default="image-style-telegram-group",
        alias="BROKER_IMAGE_STYLE_GROUP"
    )

    text_to_chatbot_topic: str = Field(
        default="text-to-chatbot",
        alias="BROKER_TEXT_TO_CHATBOT"
    )

    text_to_chatbot_result_topic: str = Field(
        default="text-to-chatbot-result",
        alias="BROKER_TEXT_TO_CHATBOT_RESULT"
    )

    text_telegram_group: str = Field(
        default="text-telegram-group",
        alias="BROKER_TEXT_TELEGRAM_GROUP"
    )

    user_create_topic: str = Field(
        default="user-create",
        alias="BROKER_USER_CREATE"
    )

    user_update_topic: str = Field(
        default="user-update",
        alias="BROKER_USER_UPDATE"
    )

    user_delete_topic: str = Field(
        default="user-delete",
        alias="BROKER_USER_DELETE"
    )

    user_successfully_linked_telegram_topic: str = Field(
        default="user-telegram-link-success",
        alias="USER_SUCCESSFULLY_LINK_TOPIC"
    )

    user_failed_link_telegram_topic: str = Field(
        default="user-telegram-link-failed",
        alias="USER_FAILED_LINK_TOPIC"
    )

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class Settings(CommonSettings):
    """
    Settings class which encapsulates logic of settings from other classes.
    In application, you must use this class.
    """

    telegram: TelegramSettings = TelegramSettings()
    cache: RedisSettings = RedisSettings()
    broker: BrokerSettings = BrokerSettings()


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()
