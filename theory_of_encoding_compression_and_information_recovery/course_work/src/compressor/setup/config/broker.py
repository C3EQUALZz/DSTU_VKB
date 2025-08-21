from pydantic import BaseModel, Field


class RabbitMQConfig(BaseModel):
    host: str = Field(
        alias="RABBITMQ_HOST",
        default="rabbitmq",
        description="RabbitMQ host",
        validate_default=True,
    )
    port: int = Field(
        alias="RABBITMQ_PORT",
        default=5672,
        description="RabbitMQ port",
        validate_default=True,
    )
    login: str = Field(
        alias="RABBITMQ_USER",
        default="guest",
        description="RabbitMQ username",
        validate_default=True,
    )
    password: str = Field(
        alias="RABBITMQ_PASS",
        default="guest",
        description="RabbitMQ password",
        validate_default=True,
    )

    @property
    def uri(self) -> str:
        return f"amqp://{self.login}:{self.password}@{self.host}:{self.port}"