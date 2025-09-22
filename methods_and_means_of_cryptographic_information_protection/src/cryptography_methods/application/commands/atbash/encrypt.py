import logging
from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.atbash import AtbashEncryptionView
from cryptography_methods.domain.atbash.services.atbash_service import AtbashService
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.values.text import Text

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class AtbashEncryptCommand:
    text: str


@final
class AtbashEncryptCommandHandler:
    def __init__(self, atbash_service: AtbashService, alphabet_service: AlphabetService) -> None:
        self._atbash_service: AtbashService = atbash_service
        self._alphabet_service: AlphabetService = alphabet_service

    async def __call__(self, data: AtbashEncryptCommand) -> AtbashEncryptionView:
        logger.info("Started encryption using Atbash algorithm. Text - %s", data.text)
        text_for_encryption: Text = Text(data.text)
        logger.info("Successfully validated text. Text - %s", text_for_encryption)

        encrypted_text: Text = self._atbash_service.encrypt(text=text_for_encryption)

        return AtbashEncryptionView(
            encrypted_text=encrypted_text.value,
            language=self._alphabet_service.get_language_from_the_text(text_for_encryption).value,
            original_text=text_for_encryption.value,
        )
