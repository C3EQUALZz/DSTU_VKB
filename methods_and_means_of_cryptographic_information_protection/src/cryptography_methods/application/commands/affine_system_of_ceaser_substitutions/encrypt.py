from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.affine_system_of_ceaser_substitution import (
    AffineSystemOfCeaserSubstitutionEncryptionView
)
from cryptography_methods.domain.ceaser.services.affine_cipher_service import AffineCipherService
from cryptography_methods.domain.ceaser.values.key_affine import KeyAffine
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.values.text import Text


@dataclass(frozen=True, slots=True)
class AffineSystemOfCeaserSubstitutionEncryptCommand:
    a: int
    b: int
    text: str


@final
class AffineSystemOfCeaserSubstitutionEncryptCommandHandler:
    def __init__(
            self,
            alphabet_service: AlphabetService,
            affine_cipher_service: AffineCipherService
    ) -> None:
        self._alphabet_service: Final[AlphabetService] = alphabet_service
        self._affine_cipher_service: Final[AffineCipherService] = affine_cipher_service

    async def __call__(
            self,
            data: AffineSystemOfCeaserSubstitutionEncryptCommand
    ) -> AffineSystemOfCeaserSubstitutionEncryptionView:
        text_for_encryption: Text = Text(data.text.strip())

        alphabet: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=text_for_encryption,
        )

        length_of_alphabet: int = len(alphabet)

        key_for_encryption: KeyAffine = KeyAffine(
            a=data.a,
            b=data.b,
            m=length_of_alphabet,
        )

        encrypted_text: str = self._affine_cipher_service.encrypt(
            key=key_for_encryption,
            text=text_for_encryption,
        )

        return AffineSystemOfCeaserSubstitutionEncryptionView(
            original_text=data.text,
            encrypted_text=encrypted_text,
            a=data.a,
            b=data.b,
            m=length_of_alphabet,
        )
