from abc import ABC
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings, ABC):
    """
    Класс, от которого каждая настройка должна наследоваться.
    Написано с той целью, чтобы не было дублирования кода по настройке model_config.
    """

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class BrokerSettings(CommonSettings):
    host: str = Field(alias="BROKER_HOST")
    port: int = Field(alias="BROKER_PORT_NETWORK")

    text_translate_topic: str = Field(default="text-translate", alias="BROKER_TEXT_TRANSLATE_TOPIC")
    text_chatbot_topic: str = Field(default="text-to-chatbot", alias="BROKER_TEXT_CHATBOT_TOPIC")
    text_chatbot_result_topic: str = Field(default="text-to-chatbot-result", alias="BROKER_TEXT_TOTAL_RESULT_TOPIC")

    text_chatbot_group_id: str = Field(default="text-chatbot", alias="BROKER_TEXT_CHATBOT_GROUP_ID")


    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class OpenAISettings(CommonSettings):
    base_url: str = Field(alias="OPENAI_BASE_URL")
    api_key: str = Field(alias="OPENAI_API_KEY")
    default_model: str = Field(alias="OPENAI_DEFAULT_MODEL", default="deepseek/deepseek-chat")


class Settings(CommonSettings):
    """
    Класс настроек, которым в дальнейшем будет оперировать приложение.
    """

    broker: BrokerSettings = BrokerSettings()
    openai: OpenAISettings = OpenAISettings()


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()
