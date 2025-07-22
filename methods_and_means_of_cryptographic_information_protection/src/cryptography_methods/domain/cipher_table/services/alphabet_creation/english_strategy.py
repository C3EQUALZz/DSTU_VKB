import logging
from string import ascii_letters
from typing import Final

from typing_extensions import override

from cryptography_methods.domain.cipher_table.services.alphabet_creation.base import AlphabetCreationStrategy

logger: Final[logging.Logger] = logging.getLogger(__name__)


class EnglishAlphabetCreationStrategy(AlphabetCreationStrategy):
    @override
    def create(self) -> str:
        logger.info("Returning ascii letters for english alphabet")
        return ascii_letters
