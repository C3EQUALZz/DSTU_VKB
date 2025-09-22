from dataclasses import dataclass
from typing import final

from cryptography_methods.application.common.views.atbash import AtbashEncryptionView
from cryptography_methods.domain.atbash.services.atbash_service import AtbashService
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.values.text import Text


@dataclass(frozen=True, slots=True)
class AtbashEncryptCommand:
    text: str


@final
class AtbashEncryptCommandHandler:
    def __init__(self, atbash_service: AtbashService, alphabet_service: AlphabetService) -> None:
        self._atbash_service: AtbashService = atbash_service
        self._alphabet_service: AlphabetService = alphabet_service

    async def __call__(self, data: AtbashEncryptCommand) -> AtbashEncryptionView:
        text_for_encryption: Text = Text(data.text)

        encrypted_text: Text = self._atbash_service.encrypt(text=text_for_encryption)

        return AtbashEncryptionView(
            encrypted_text=encrypted_text.value,
            language=self._alphabet_service.get_language_from_the_text(text_for_encryption).value,
            original_text=text_for_encryption.value,
        )
