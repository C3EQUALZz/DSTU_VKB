from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.ceaser_classic import CeaserClassicEncryptionView
from cryptography_methods.domain.ceaser.services.classic_ceaser_service import ClassicCeaserService
from cryptography_methods.domain.ceaser.values.key_classic_caesar import KeyClassicCaesar
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.values.languages import LanguageType
from cryptography_methods.domain.common.values.text import Text


@dataclass(frozen=True, slots=True)
class CeaserClassicEncryptCommand:
    key: int
    text: str


@final
class CeaserClassicEncryptCommandHandler:
    def __init__(
            self,
            classic_ceaser_service: ClassicCeaserService,
            alphabet_service: AlphabetService,
    ) -> None:
        self._classic_ceaser_service: Final[ClassicCeaserService] = classic_ceaser_service
        self._alphabet_service: Final[AlphabetService] = alphabet_service

    async def __call__(self, data: CeaserClassicEncryptCommand) -> CeaserClassicEncryptionView:
        validated_text: Text = Text(data.text)

        alphabet_type: LanguageType = self._alphabet_service.get_language_from_the_text(
            text=validated_text
        )

        key_for_classic_caesar: KeyClassicCaesar = KeyClassicCaesar(
            value=data.key,
            alphabet=alphabet_type
        )

        encoded_string: str = self._classic_ceaser_service.encrypt(
            key=key_for_classic_caesar,
            text=validated_text
        )

        return CeaserClassicEncryptionView(
            original_text=data.text,
            encrypted_text=encoded_string,
            key=data.key,
        )
