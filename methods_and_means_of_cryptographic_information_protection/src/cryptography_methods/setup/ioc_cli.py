from typing import Final, Iterable

from dishka import Provider, Scope

from cryptography_methods.application.commands.simple_table_permutation.decrypt import (
    SimpleTablePermutationDecryptCommandHandler
)
from cryptography_methods.application.commands.simple_table_permutation.encrypt import (
    SimpleTablePermutationEncryptCommandHandler
)
from cryptography_methods.domain.cipher_table.services.cipher_table_service import CipherTableService
from cryptography_methods.domain.cipher_table.services.id_generator import CipherTableIdGenerator
from cryptography_methods.domain.cipher_table.services.simple_table_permutation_service import (
    SimpleTablePermutationService
)
from cryptography_methods.infrastructure.adapters.uuid_4_cipher_table_id_generator import UUID4CipherTableIdGenerator


def interactors_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide_all(
        SimpleTablePermutationDecryptCommandHandler,
        SimpleTablePermutationEncryptCommandHandler,
    )
    return provider


def id_generators_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide(UUID4CipherTableIdGenerator, provides=CipherTableIdGenerator)
    return provider


def services_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide_all(
        CipherTableService,
        SimpleTablePermutationService
    )
    return provider


def setup_providers() -> Iterable[Provider]:
    return (
        interactors_provider(),
        id_generators_provider(),
        services_provider(),
    )
