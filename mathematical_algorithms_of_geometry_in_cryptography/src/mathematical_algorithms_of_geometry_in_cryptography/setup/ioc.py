from typing import Final, Iterable

from dishka import Provider, Scope

from mathematical_algorithms_of_geometry_in_cryptography.application.commands.find_divisor import \
    FindDivisorCommandHandler
from mathematical_algorithms_of_geometry_in_cryptography.application.commands.miller_rabit_test import (
    MakeMillerRabitTestCommandHandler
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin import MillerRabinService
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.ports.miller_rabin_id_generator import (
    MillerRabinIDGenerator
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho import PollardRhoService
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.ports.pollard_rho_id_generator import (
    PollardRhoIDGenerator
)
from mathematical_algorithms_of_geometry_in_cryptography.infrastructure.adapters.uuid4_miller_rabin_id_generator import (
    UUID4MillerRabinIDGenerator
)
from mathematical_algorithms_of_geometry_in_cryptography.infrastructure.adapters.uuid4_pollard_rho_id_generator import (
    UUID4PollardRhoIDGenerator
)


def id_generators_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide(source=UUID4MillerRabinIDGenerator, provides=MillerRabinIDGenerator)
    provider.provide(source=UUID4PollardRhoIDGenerator, provides=PollardRhoIDGenerator)
    return provider


def services_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide_all(
        MillerRabinService,
        PollardRhoService
    )
    return provider


def interactors_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)

    provider.provide_all(
        MakeMillerRabitTestCommandHandler,
        FindDivisorCommandHandler
    )

    return provider


def setup_providers() -> Iterable[Provider]:
    return (
        id_generators_provider(),
        services_provider(),
        interactors_provider(),
    )
