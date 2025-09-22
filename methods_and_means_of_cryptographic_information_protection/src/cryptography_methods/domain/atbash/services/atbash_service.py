from collections import deque
from string import punctuation
from typing import Final

from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.common.values.text import Text


class AtbashService(DomainService):
    def __init__(self, alphabet_service: AlphabetService) -> None:
        super().__init__()
        self._alphabet_service: Final[AlphabetService] = alphabet_service

    def encrypt(self, text: Text) -> Text:
        alphabet: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=text
        )

        deque_with_encrypted_text: deque[str] = deque()

        for alpha in text:
            if alpha in punctuation:
                deque_with_encrypted_text.append(alpha)
            else:
                deque_with_encrypted_text.append(alphabet[~alphabet.index(alpha)])

        return Text("".join(deque_with_encrypted_text))

    def decrypt(self, text: Text) -> Text:
        alphabet: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=text
        )

        deque_with_encrypted_text: deque[str] = deque()

        for alpha in text:
            if alpha in punctuation:
                deque_with_encrypted_text.append(alpha)
            else:
                deque_with_encrypted_text.append(alphabet[~alphabet.index(alpha)])

        return Text("".join(deque_with_encrypted_text))
