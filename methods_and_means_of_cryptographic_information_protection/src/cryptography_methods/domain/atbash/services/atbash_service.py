import logging
from collections import deque
from string import punctuation
from typing import Final

from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.common.values.text import Text

logger: Final[logging.Logger] = logging.getLogger(__name__)


class AtbashService(DomainService):
    def __init__(self, alphabet_service: AlphabetService) -> None:
        super().__init__()
        self._alphabet_service: Final[AlphabetService] = alphabet_service

    def encrypt(self, text: Text) -> Text:
        logger.info("Started building alphabet for encryption....")

        alphabet: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=text
        )

        logger.info("Alphabet - %s", alphabet)

        deque_with_encrypted_text: deque[str] = deque()

        for alpha in text:
            logger.info("Processing alpha - %s", alpha)
            if alpha in punctuation or alpha.isspace():
                logger.info("Current alpha is punctuation - %s", alpha)
                deque_with_encrypted_text.append(alpha)
            else:
                index_of_new_alpha: int = alphabet.index(alpha.lower() if alpha.isupper() else alpha)
                logger.info("New index of alpha - %s", index_of_new_alpha)
                new_letter: str = alphabet[~index_of_new_alpha]
                logger.info("New letter - %s", new_letter)
                deque_with_encrypted_text.append(new_letter)

        return Text("".join(deque_with_encrypted_text))

    def decrypt(self, text: Text) -> Text:
        alphabet: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=text
        )

        deque_with_encrypted_text: deque[str] = deque()

        for alpha in text:
            if alpha in punctuation or alpha.isspace():
                deque_with_encrypted_text.append(alpha)
            else:
                index_of_new_alpha: int = alphabet.index(alpha)
                new_letter: str = alphabet[~index_of_new_alpha]
                deque_with_encrypted_text.append(new_letter)

        return Text("".join(deque_with_encrypted_text))
