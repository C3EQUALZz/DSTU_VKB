from typing import Iterable, Final

from dishka import Provider, Scope

from cryptography_methods.setup.settings import (
    PostgresConfig,
    SQLAlchemyConfig,
    RedisConfig
)


def configs_provider() -> Provider:
    """Creates a Provider for application configuration dependencies.

    Provides:
        - ASGIConfig (app-scoped)
        - PostgresConfig (app-scoped)

    Returns:
        Provider: Configured provider instance with application-level configs.
    """
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.from_context(provides=PostgresConfig)
    provider.from_context(provides=SQLAlchemyConfig)
    provider.from_context(provides=RedisConfig)
    return provider


def interactors_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)


def setup_providers() -> Iterable[Provider]:
    return (
        configs_provider(),
    )
