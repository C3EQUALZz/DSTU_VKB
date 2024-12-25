import os.path
from abc import ABC

from pydantic import (
    Field,
    MongoDsn,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class CommonSettings(BaseSettings, ABC):
    """
    Класс, от которого каждая настройка должна наследоваться.
    Написано с той целью, чтобы не было дублирования кода по настройке model_config.
    """
    model_config = SettingsConfigDict(
        env_file=os.path.expanduser("database_management_systems/8/backend/.env"),
        env_file_encoding="utf-8",
        extra="allow"
    )


class AuthSettings(CommonSettings):
    """
    Общие настройки аутентификации
    """

    private_key: str = Field(alias="PRIVATE_KEY")
    public_key: str = Field(alias="PUBLIC_KEY")
    algorithm: str = Field(default="RS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=5, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_minutes: int = Field(default=10, alias="REFRESH_TOKEN_EXPIRE_MINUTES")


class MongoSettings(CommonSettings):
    database_name: str = Field(alias="MONGO_DB_DATABASE_NAME")
    url: MongoDsn = Field(alias="MONGO_DB_URL")


class Settings(CommonSettings):
    auth: AuthSettings = AuthSettings()
    database: MongoSettings = MongoSettings()
