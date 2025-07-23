import logging
import string
from collections import deque
from typing import Final

from cryptography_methods.domain.ceaser.errors import CantFindModularInverse
from cryptography_methods.domain.ceaser.values.key_affine import KeyAffine
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.common.values.text import Text

logger: Final[logging.Logger] = logging.getLogger(__name__)


class AffineCipherService(DomainService):
    def __init__(
            self,
            alphabet_service: AlphabetService
    ) -> None:
        super().__init__()
        self._alphabet_service: Final[AlphabetService] = alphabet_service

    def encrypt(self, key: KeyAffine, text: Text) -> str:
        a: int = key.a
        b: int = key.b
        m: int = key.m

        logger.info(f"Got keys for encryption: {a=}, {b=}, {m=}")

        alphabet: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=text,
            uppercase_symbols=False
        )

        result: deque[str] = deque()

        for char in text:
            logger.info("Processing character %s", char)

            if char in string.punctuation + string.whitespace:
                logger.info("Character is punctuation symbol or space, skipping decryption this char...")
                result.append(char)
                continue

            new_index: int = (a * alphabet.index(char.lower()) + b) % m
            logger.info("New index is %d", new_index)
            new_char: str = alphabet[new_index].upper() if char.isupper() else alphabet[new_index]

            logger.info("New char is %s", new_char)
            result.append(new_char)

        return "".join(result)

    def decrypt(self, key: KeyAffine, text: Text) -> str:
        a: int = key.a
        b: int = key.b
        m: int = key.m

        logger.info(f"Got keys for encryption: {a=}, {b=}, {m=}")

        alphabet: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=text,
            uppercase_symbols=False
        )

        result: deque[str] = deque()

        for char in text:
            logger.info("Processing character %s", char)

            if char in string.punctuation + string.whitespace:
                logger.info("Character is punctuation symbol or space, skipping decryption this char...")
                result.append(char)
                continue

            new_index: int = self.__find_modular_inverse(a, m) * (alphabet.index(char.lower()) - b) % m
            logger.info("New index is %d", new_index)
            new_char: str = alphabet[new_index].upper() if char.isupper() else alphabet[new_index]
            logger.info("New char is %s", new_char)
            result.append(new_char)

        return "".join(result)

    @staticmethod
    def __find_modular_inverse(
            multiplier: int,
            modulus: int
    ) -> int:
        """
        Находит модульный обратный элемент для multiplier по модулю modulus.

        Args:
            multiplier (int): Число, для которого ищем обратный элемент (обычно 'a' из ключа)
            modulus (int): Модуль (размер алфавита)
        """
        for candidate in range(modulus):
            if ((multiplier % modulus) * (candidate % modulus)) % modulus == 1:
                return candidate
        raise CantFindModularInverse(f"Cant find modular inverse for {multiplier=}, {modulus=}")
