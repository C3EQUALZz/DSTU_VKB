from typing import Final, Iterable

from dishka import Provider, Scope

from cryptography_methods.application.commands.ceaser_classic.decrypt import CeaserClassicDecryptCommandHandler
from cryptography_methods.application.commands.ceaser_classic.encrypt import CeaserClassicEncryptCommandHandler
from cryptography_methods.application.commands.simple_table_permutation.decrypt import (
    SimpleTablePermutationDecryptCommandHandler
)
from cryptography_methods.application.commands.simple_table_permutation.encrypt import (
    SimpleTablePermutationEncryptCommandHandler
)
from cryptography_methods.application.commands.single_key_permutation.decrypt import (
    SingleKeyPermutationDecryptCommandHandler
)
from cryptography_methods.application.commands.single_key_permutation.encrypt import (
    SingleKeyPermutationEncryptCommandHandler
)
from cryptography_methods.domain.ceaser.services.classic_ceaser_service import ClassicCeaserService
from cryptography_methods.domain.cipher_table.services.cipher_table_service import CipherTableService
from cryptography_methods.domain.cipher_table.services.id_generator import CipherTableIdGenerator
from cryptography_methods.domain.cipher_table.services.simple_table_permutation_service import (
    SimpleTablePermutationService
)
from cryptography_methods.domain.cipher_table.services.single_key_permutation_service import (
    SingleKeyPermutationService
)
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.infrastructure.adapters.uuid_4_cipher_table_id_generator import (
    UUID4CipherTableIdGenerator
)


def interactors_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide_all(
        SimpleTablePermutationDecryptCommandHandler,
        SimpleTablePermutationEncryptCommandHandler,
        SingleKeyPermutationEncryptCommandHandler,
        SingleKeyPermutationDecryptCommandHandler,
        CeaserClassicEncryptCommandHandler,
        CeaserClassicDecryptCommandHandler
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
        SimpleTablePermutationService,
        SingleKeyPermutationService,
        ClassicCeaserService,
        AlphabetService
    )
    return provider


def setup_providers() -> Iterable[Provider]:
    return (
        interactors_provider(),
        id_generators_provider(),
        services_provider(),
    )
