from pydantic import BaseModel, Field


class TGConfig(BaseModel):
    bot_token: str = Field(..., alias="BOT_TOKEN", description="Telegram bot token")
    use_redis_storage: bool = True
    use_redis_event_isolation: bool = True
    use_i18n_isolation: bool = True
    default_locale: str = "ru"
