from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.vigenere import VigenereDecryptView
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.values.text import Text
from cryptography_methods.domain.vigenere.services.vigenere_service import VigenereService


@dataclass(frozen=True, slots=True)
class VigenereDecryptCommand:
    text: str
    key: str


@final
class VigenereDecryptCommandHandler:
    def __init__(
            self,
            alphabet_service: AlphabetService,
            vigenere_service: VigenereService,
    ) -> None:
        self._alphabet_service: Final[AlphabetService] = alphabet_service
        self._vigenere_service: Final[VigenereService] = vigenere_service

    async def __call__(self, data: VigenereDecryptCommand) -> VigenereDecryptView:
        keyword: Text = Text(data.key)
        text_for_encryption: Text = Text(data.text)

        length_of_alphabet: int = len(self._alphabet_service.build_alphabet_by_provided_text(
            text=text_for_encryption
        ))

        decrypted_text: Text = self._vigenere_service.decrypt(
            key=keyword,
            text=text_for_encryption,
        )

        return VigenereDecryptView(
            original_text=text_for_encryption.value,
            decrypted_text=decrypted_text.value,
            key=data.key,
            length_of_alphabet=length_of_alphabet
        )
