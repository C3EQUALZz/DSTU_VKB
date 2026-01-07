from pydantic import BaseModel, Field, field_validator

from chat_service.setup.config.consts import PORT_MAX, PORT_MIN


class ASGIConfig(BaseModel):
    """Configuration container for ASGI server settings.

    Attributes:
        host: Interface to bind the server to (e.g., '0.0.0.0' or 'localhost').
        port: TCP port to listen on.
    """

    host: str = Field(
        alias="UVICORN_HOST",
        default="0.0.0.0", # nosec B104
        description="Interface to bind the server to (e.g., '0.0.0.0' or 'localhost').",
        validate_default=True,
    )
    port: int = Field(
        alias="UVICORN_PORT",
        default=8080,
        description="TCP port to listen on.",
        validate_default=True,
    )

    fastapi_debug: bool = Field(
        alias="FASTAPI_DEBUG",
        default=True,
        description="Enable fastapi debug output.",
        validate_default=True,
    )
    allow_credentials: bool = Field(
        alias="FASTAPI_ALLOW_CREDENTIALS",
        default=False,
        description="Enable fastapi allow credentials.",
        validate_default=True,
    )
    allow_methods: list[str] = [
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE"
    ]
    allow_headers: list[str] = [
        "Authorization",
        "Content-Type",
        "Cache-Control",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
    ]

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        if not PORT_MIN <= v <= PORT_MAX:
            raise ValueError(
                f"UVICORN_PORT must be between {PORT_MIN} and {PORT_MAX}, got {v}."
            )
        return v