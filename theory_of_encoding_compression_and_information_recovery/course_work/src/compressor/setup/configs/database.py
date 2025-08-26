from pydantic import BaseModel, Field, PostgresDsn


class PostgresConfig(BaseModel):
    """Configuration container for PostgreSQL database connection settings.

    Attributes:
        user: Database username.
        password: Database password.
        host: Database server hostname or IP address.
        port: Database server port.
        db_name: Name of the database to connect to.

    Properties:
        uri: Complete PostgreSQL connection URI in psycopg format.
    """

    user: str = Field(
        alias="POSTGRES_USER",
        description="Database username to connect",
    )
    password: str = Field(
        alias="POSTGRES_PASSWORD",
        description="Database password to connect",
    )
    host: str = Field(
        alias="POSTGRES_HOST",
        description="Database server hostname or IP address",
    )
    port: int = Field(
        alias="POSTGRES_PORT",
        description="Database server port",
    )
    db_name: str = Field(
        alias="POSTGRES_DB",
        description="Database name to connect",
    )
    driver: str = Field(
        alias="POSTGRES_DRIVER",
        description="Database driver name",
    )

    @property
    def uri(self) -> str:
        """Generates a PostgreSQL connection URI.

        Returns:
            str: Connection string in format:
                postgresql+psycopg://user:password@host:port/db_name

        Note:
            - Uses psycopg driver for async operations
            - Includes all authentication credentials
            - Suitable for SQLAlchemy's create_async_engine
        """
        return str(
            PostgresDsn.build(
                scheme=f"postgresql+{self.driver}",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.db,
            ),
        )


class SQLAlchemyConfig(BaseModel):
    """
    Configuration container for SQLAlchemy.

    Attributes:
        debug: Flag to enable debug output for database operations.
    """
    pool_pre_ping: bool = Field(
        alias="DB_POOL_PRE_PING",
        default=True,
        description="Enable database pool pre ping.",
        validate_default=True,
    )
    pool_recycle: int = Field(
        alias="DB_POOL_RECYCLE",
        default=3600,
        description="Count of database connection pools",
    )
    echo: bool = Field(
        alias="DB_ECHO",
        default=False,
        description="Enable database echo mode for debugging.",
        validate_default=True,
    )
    auto_flush: bool = Field(
        alias="DB_AUTO_FLUSH",
        default=False,
        description="Enable database auto flush mode",
        validate_default=True,
    )
    expire_on_commit: bool = Field(
        alias="DB_EXPIRE_ON_COMMIT",
        default=False,
        description="Enable database expire on commit mode",
        validate_default=True,
    )
    future: bool = Field(
        alias="DB_FUTURE",
        default=True,
        description="Enable database future mode.",
        validate_default=True,
    )
