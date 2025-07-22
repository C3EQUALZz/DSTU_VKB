import logging
from string import ascii_lowercase, ascii_uppercase
from typing import Final

from typing_extensions import override

from cryptography_methods.domain.cipher_table.services.alphabet_creation.base import AlphabetCreationStrategy

logger: Final[logging.Logger] = logging.getLogger(__name__)


class EnglishAlphabetCreationStrategy(AlphabetCreationStrategy):
    @override
    def create(self, uppercase_symbols: bool = False) -> str:
        if uppercase_symbols:
            logger.info("Returning ascii uppercase letters for english alphabet")
            return ascii_uppercase

        logger.info("Returning ascii lowercase letters for english alphabet")
        return ascii_lowercase
