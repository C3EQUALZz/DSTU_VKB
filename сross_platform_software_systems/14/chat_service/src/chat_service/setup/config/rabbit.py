from pydantic import AmqpDsn, BaseModel, Field, field_validator

from chat_service.setup.config.consts import PORT_MAX, PORT_MIN


class RabbitConfig(BaseModel):
    """Configuration container for RabbitMQ connection settings.

        Attributes:
            user: rabbitmq username.
            password: rabbitmq password.
            host: rabbitmq hostname or IP address.
            port: rabbitmq server port.

        Properties:
            uri: Complete RabbitMQ connection URI.
    """
    host: str = Field(
        alias="RABBITMQ_HOST",
        description="RabbitMQ host name or IP address.",
    )
    port: int = Field(
        alias="RABBITMQ_PORT",
        description="RabbitMQ server port.",
    )
    user: str = Field(
        alias="RABBITMQ_DEFAULT_USER",
        description="Default RabbitMQ username.",
    )
    password: str = Field(
        alias="RABBITMQ_DEFAULT_PASS",
        description="Default RabbitMQ password.",
    )

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        if not PORT_MIN <= v <= PORT_MAX:
            raise ValueError(
                f"RABBITMQ_PORT must be between {PORT_MIN} and {PORT_MAX}, got {v}."
            )
        return v

    @property
    def uri(self) -> str:
        """Generates a RabbitMQ connection URI.

        Returns:
            str: Connection string in format

        Note:
            - Includes all authentication credentials
        """
        return str(
            AmqpDsn.build(
                scheme="amqp",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            ),
        )