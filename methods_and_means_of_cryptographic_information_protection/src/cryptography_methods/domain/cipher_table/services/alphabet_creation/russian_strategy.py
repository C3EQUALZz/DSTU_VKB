import logging
from typing import Final

from typing_extensions import override

from cryptography_methods.domain.cipher_table.services.alphabet_creation.base import AlphabetCreationStrategy

logger: Final[logging.Logger] = logging.getLogger(__name__)


class RussianAlphabetCreationStrategy(AlphabetCreationStrategy):
    @override
    def create(self, uppercase_symbols: bool = False) -> str:
        start_value: int = ord('а')
        first_part: list[str] = [chr(i) for i in range(start_value, start_value + 6)]
        middle_part: list[str] = [chr(start_value + 33)]
        last_part: list[str] = [chr(i) for i in range(start_value + 6, start_value + 32)]
        lowercase_letters: str = ''.join(first_part + middle_part + last_part)

        if uppercase_symbols:
            uppercase_letters: str = lowercase_letters.upper()
            logger.info("Returning russian uppercase letters")
            return uppercase_letters

        logger.info("Returning russian lowercase letters")

        return lowercase_letters
