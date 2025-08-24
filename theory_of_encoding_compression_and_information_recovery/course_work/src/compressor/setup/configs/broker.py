from pydantic import BaseModel, Field, AmqpDsn


class RabbitMQConfig(BaseModel):
    host: str = Field(
        alias="RABBITMQ_HOST",
        description="RabbitMQ host",
        validate_default=True,
    )
    port: int = Field(
        alias="RABBITMQ_PORT",
        description="RabbitMQ port",
        validate_default=True,
    )
    login: str = Field(
        alias="RABBITMQ_DEFAULT_USER",
        description="RabbitMQ username",
        validate_default=True,
    )
    password: str = Field(
        alias="RABBITMQ_DEFAULT_PASS",
        description="RabbitMQ password",
        validate_default=True,
    )

    @property
    def uri(self) -> str:
        return str(
            AmqpDsn(
                url=f"amqp://{self.login}:{self.password}@{self.host}:{self.port}"
            )
        )