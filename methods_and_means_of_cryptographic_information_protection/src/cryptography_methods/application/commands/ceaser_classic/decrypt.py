from dataclasses import dataclass
from typing import Final, final

from cryptography_methods.application.common.views.ceaser_classic import CeaserClassicDecryptionView
from cryptography_methods.domain.ceaser.services.classic_ceaser_service import ClassicCeaserService
from cryptography_methods.domain.ceaser.values.key_classic_caesar import KeyClassicCaesar
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.values.languages import LanguageType
from cryptography_methods.domain.common.values.text import Text


@dataclass(frozen=True, slots=True)
class CeaserClassicDecryptCommand:
    key: int
    text: str


@final
class CeaserClassicDecryptCommandHandler:
    def __init__(
            self,
            classic_ceaser_service: ClassicCeaserService,
            alphabet_service: AlphabetService,
    ) -> None:
        self._classic_ceaser_service: Final[ClassicCeaserService] = classic_ceaser_service
        self._alphabet_service: Final[AlphabetService] = alphabet_service

    async def __call__(self, data: CeaserClassicDecryptCommand) -> CeaserClassicDecryptionView:
        validated_text: Text = Text(data.text)

        alphabet_type: LanguageType = self._alphabet_service.get_language_from_the_text(
            text=validated_text
        )

        key_for_classic_caesar: KeyClassicCaesar = KeyClassicCaesar(
            value=data.key,
            alphabet=alphabet_type
        )

        decoded_string: str = self._classic_ceaser_service.decrypt(
            key=key_for_classic_caesar,
            text=validated_text
        )

        return CeaserClassicDecryptionView(
            key=data.key,
            original_text=data.text,
            decrypted_text=decoded_string,
        )
