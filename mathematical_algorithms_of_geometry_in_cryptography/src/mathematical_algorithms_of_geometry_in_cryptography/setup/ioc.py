from typing import Final, Iterable

from dishka import Provider, Scope

from mathematical_algorithms_of_geometry_in_cryptography.application.commands.miller_rabit_test import (
    MakeMillerRabitTestCommandHandler
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin import MillerRabinService
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.ports.miller_rabin_id_generator import (
    MillerRabinIDGenerator
)
from mathematical_algorithms_of_geometry_in_cryptography.infrastructure.adapters.uuid4_miller_rabin_id_generator import (
    UUID4MillerRabinIDGenerator
)


def id_generators_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide(source=UUID4MillerRabinIDGenerator, provides=MillerRabinIDGenerator)
    return provider


def services_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide(MillerRabinService)
    return provider


def interactors_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)

    provider.provide_all(
        MakeMillerRabitTestCommandHandler
    )

    return provider


def setup_providers() -> Iterable[Provider]:
    return (
        id_generators_provider(),
        services_provider(),
        interactors_provider(),
    )
