from typing import Final

from dishka import Provider, Scope

from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.ports.miller_rabin_id_generator import \
    MillerRabinIDGenerator
from mathematical_algorithms_of_geometry_in_cryptography.infrastructure.adapters.uuid4_miller_rabin_id_generator import \
    UUID4MillerRabinIDGenerator


def id_generators_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide(source=UUID4MillerRabinIDGenerator, provides=MillerRabinIDGenerator)
    return provider
