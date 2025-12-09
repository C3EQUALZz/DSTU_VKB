from typing import Final, Iterable

from dishka import Provider, Scope

from cryptography_methods.application.commands.affine_system_of_ceaser_substitutions.decrypt import (
    AffineSystemOfCeaserSubstitutionDecryptCommandHandler
)
from cryptography_methods.application.commands.affine_system_of_ceaser_substitutions.encrypt import (
    AffineSystemOfCeaserSubstitutionEncryptCommandHandler
)
from cryptography_methods.application.commands.atbash.decrypt import AtbashDecryptCommandHandler
from cryptography_methods.application.commands.atbash.encrypt import AtbashEncryptCommandHandler
from cryptography_methods.application.commands.ceaser_classic.decrypt import CeaserClassicDecryptCommandHandler
from cryptography_methods.application.commands.ceaser_classic.encrypt import CeaserClassicEncryptCommandHandler
from cryptography_methods.application.commands.ceaser_keyword.decrypt import CeaserKeywordDecryptCommandHandler
from cryptography_methods.application.commands.ceaser_keyword.encrypt import CeaserKeywordEncryptCommandHandler
from cryptography_methods.application.commands.double_square_whitestone.decrypt import \
    DecryptDoubleSquareWhitestoneCommandHandler
from cryptography_methods.application.commands.double_square_whitestone.encrypt import \
    EncryptDoubleSquareWhitestoneCommandHandler
from cryptography_methods.application.commands.linear_feedback_shift_register.mutate import \
    MutateLinearFeedbackShiftRegisterCommandHandler
from cryptography_methods.application.commands.magic_table.decrypt import MagicTableDecryptCommandHandler
from cryptography_methods.application.commands.magic_table.encrypt import MagicTableEncryptCommandHandler
from cryptography_methods.application.commands.playfair.decrypt import PlayfairDecryptCommandHandler
from cryptography_methods.application.commands.playfair.encrypt import PlayfairEncryptCommandHandler
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
from cryptography_methods.application.commands.trithemius.decrypt import TrithemiusDecryptCommandHandler
from cryptography_methods.application.commands.trithemius.encrypt import TrithemiusEncryptCommandHandler
from cryptography_methods.application.commands.vigenere.decrypt import VigenereDecryptCommandHandler
from cryptography_methods.application.commands.vigenere.encrypt import VigenereEncryptCommandHandler
from cryptography_methods.domain.atbash.services.atbash_service import AtbashService
from cryptography_methods.domain.ceaser.services.affine_cipher_service import AffineCipherService
from cryptography_methods.domain.ceaser.services.ceaser_keyword_service import CeaserKeywordService
from cryptography_methods.domain.ceaser.services.classic_ceaser_service import ClassicCeaserService
from cryptography_methods.domain.ceaser.services.trithemius_service import TrithemiusService
from cryptography_methods.domain.cipher_table.services.cipher_table_service import CipherTableService
from cryptography_methods.domain.cipher_table.services.id_generator import CipherTableIdGenerator
from cryptography_methods.domain.cipher_table.services.magic_table_service import MagicTableService
from cryptography_methods.domain.cipher_table.services.simple_table_permutation_service import (
    SimpleTablePermutationService
)
from cryptography_methods.domain.cipher_table.services.single_key_permutation_service import (
    SingleKeyPermutationService
)
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.double_square_whitestone.services.double_square_whitestone_service import \
    DoubleSquareWhitestoneService
from cryptography_methods.domain.double_square_whitestone.services.id_generator import DoubleTableWhitestoneIdGenerator
from cryptography_methods.domain.linear_feedback_shift_register.services.id_generator import \
    LinearFeedbackShiftRegisterGeneratorID
from cryptography_methods.domain.linear_feedback_shift_register.services.linear_feedback_shift_register_service import \
    LinearFeedbackShiftRegisterService
from cryptography_methods.domain.playfair.services.playfair_service import PlayfairService
from cryptography_methods.domain.vigenere.services.vigenere_service import VigenereService
from cryptography_methods.infrastructure.adapters.uuid_4_cipher_table_id_generator import (
    UUID4CipherTableIdGenerator
)
from cryptography_methods.infrastructure.adapters.uuid_4_linear_feedback_register_id_generator import \
    UUID4LinearFeedbackRegisterIDGenerator
from cryptography_methods.infrastructure.adapters.uuid_4_table_whitestone_id_generator import \
    UUID4TableWhiteStoneIDGenerator


def interactors_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide_all(
        SimpleTablePermutationDecryptCommandHandler,
        SimpleTablePermutationEncryptCommandHandler,
        SingleKeyPermutationEncryptCommandHandler,
        SingleKeyPermutationDecryptCommandHandler,
        CeaserClassicEncryptCommandHandler,
        CeaserClassicDecryptCommandHandler,
        AffineSystemOfCeaserSubstitutionEncryptCommandHandler,
        AffineSystemOfCeaserSubstitutionDecryptCommandHandler,
        CeaserKeywordDecryptCommandHandler,
        CeaserKeywordEncryptCommandHandler,
        TrithemiusDecryptCommandHandler,
        TrithemiusEncryptCommandHandler,
        PlayfairEncryptCommandHandler,
        PlayfairDecryptCommandHandler,
        VigenereEncryptCommandHandler,
        VigenereDecryptCommandHandler,
        MagicTableDecryptCommandHandler,
        MagicTableEncryptCommandHandler,
        EncryptDoubleSquareWhitestoneCommandHandler,
        DecryptDoubleSquareWhitestoneCommandHandler,
        AtbashEncryptCommandHandler,
        AtbashDecryptCommandHandler,
        MutateLinearFeedbackShiftRegisterCommandHandler
    )
    return provider


def id_generators_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide(UUID4CipherTableIdGenerator, provides=CipherTableIdGenerator)
    provider.provide(UUID4TableWhiteStoneIDGenerator, provides=DoubleTableWhitestoneIdGenerator)
    provider.provide(UUID4LinearFeedbackRegisterIDGenerator, provides=LinearFeedbackShiftRegisterGeneratorID)
    return provider


def services_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide_all(
        CipherTableService,
        SimpleTablePermutationService,
        SingleKeyPermutationService,
        ClassicCeaserService,
        AlphabetService,
        AffineCipherService,
        CeaserKeywordService,
        TrithemiusService,
        PlayfairService,
        VigenereService,
        MagicTableService,
        DoubleSquareWhitestoneService,
        AtbashService,
        LinearFeedbackShiftRegisterService
    )
    return provider


def setup_providers() -> Iterable[Provider]:
    return (
        interactors_provider(),
        id_generators_provider(),
        services_provider(),
    )
