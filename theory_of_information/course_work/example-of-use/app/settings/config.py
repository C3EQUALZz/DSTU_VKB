from abc import ABC
from functools import lru_cache
from pathlib import Path

from pydantic import Field
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
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class DatabaseSettings(CommonSettings):
    """
    Настройки для подключения к базе данных.
    Здесь есть параметры Optional с той целью, потому что может использоваться sqlite.
    """

    host: str | None = Field(alias="DATABASE_HOST", default=None)
    port: int | None = Field(alias="DATABASE_PORT", default=None)
    user: str | None = Field(alias="DATABASE_USER", default=None)
    password: str | None = Field(alias="DATABASE_PASSWORD", default=None)
    name: str = Field(alias="DATABASE_NAME")
    dialect: str = Field(alias="DATABASE_DIALECT")
    driver: str = Field(alias="DATABASE_DRIVER")

    psql_bin_path: Path = Path(r"C:\Program Files\PostgreSQL\17\bin")

    @property
    def url(self) -> str:
        if self.dialect == "sqlite":
            return f"{self.dialect}+{self.driver}:///{self.name}"

        return f"{self.dialect}+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class MinIOSettings(CommonSettings):
    storage_engine: str = 'S3'
    bucket_name: str = "dump-database"
    bucket_backup_path: str = "postgres/"

    user: str = "your_username"
    port: int = 9000
    host: str = "localhost"
    password: str = "your_password"

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"


class Settings(CommonSettings):
    database: DatabaseSettings = DatabaseSettings()
    s3: MinIOSettings = MinIOSettings()


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()
