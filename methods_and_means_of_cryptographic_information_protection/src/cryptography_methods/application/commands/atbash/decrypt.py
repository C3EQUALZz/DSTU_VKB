from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.atbash import AtbashDecryptionView
from cryptography_methods.domain.atbash.services.atbash_service import AtbashService
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.values.text import Text


@dataclass(frozen=True, slots=True)
class AtbashDecryptCommand:
    text: str


@final
class AtbashDecryptCommandHandler:
    def __init__(self, atbash_service: AtbashService, alphabet_service: AlphabetService) -> None:
        self._atbash_service: Final[AtbashService] = atbash_service
        self._alphabet_service: Final[AlphabetService] = alphabet_service

    async def __call__(self, data: AtbashDecryptCommand) -> AtbashDecryptionView:
        text_for_decryption: Text = Text(data.text)

        decrypted_text: Text = self._atbash_service.decrypt(text=text_for_decryption)

        return AtbashDecryptionView(
            decrypted_text=decrypted_text.value,
            language=self._alphabet_service.get_language_from_the_text(text_for_decryption).value,
            original_text=text_for_decryption.value,
        )
