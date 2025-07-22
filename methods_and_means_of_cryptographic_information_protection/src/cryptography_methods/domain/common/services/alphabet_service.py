import logging
import re
from typing import Final

from cryptography_methods.domain.cipher_table.services.alphabet_creation.base import AlphabetCreationStrategy
from cryptography_methods.domain.cipher_table.services.alphabet_creation.context import AlphabetCreationContext
from cryptography_methods.domain.cipher_table.services.alphabet_creation.english_strategy import (
    EnglishAlphabetCreationStrategy
)
from cryptography_methods.domain.cipher_table.services.alphabet_creation.russian_strategy import (
    RussianAlphabetCreationStrategy
)
from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.common.values.languages import LanguageType
from cryptography_methods.domain.common.values.text import Text

logger: Final[logging.Logger] = logging.getLogger(__name__)


class AlphabetService(DomainService):
    def __init__(self) -> None:
        super().__init__()

    def build_alphabet_by_provided_language_type(
            self,
            language_type: LanguageType,
            uppercase_symbols: bool = False,
    ) -> str:
        logger.info("Building alphabet by key letters")
        strategy: AlphabetCreationStrategy
        context: AlphabetCreationContext

        if language_type is LanguageType.ENGLISH:
            strategy = EnglishAlphabetCreationStrategy()
            context = AlphabetCreationContext(strategy)
            return context(uppercase_symbols)

        if language_type is LanguageType.RUSSIAN:
            strategy = RussianAlphabetCreationStrategy()
            context = AlphabetCreationContext(strategy)
            return context(uppercase_symbols)

        logger.info("Not Implemented for this alphabet. Please check")

        raise NotImplementedError

    def build_alphabet_by_provided_text(
            self,
            text: Text,
            uppercase_symbols: bool = False,
    ) -> str:
        logger.info("Building alphabet by key letters")
        strategy: AlphabetCreationStrategy
        context: AlphabetCreationContext

        if self.get_language_from_the_text(text) is LanguageType.ENGLISH:
            strategy = EnglishAlphabetCreationStrategy()
            context = AlphabetCreationContext(strategy)
            return context(uppercase_symbols)

        if self.get_language_from_the_text(text) is LanguageType.RUSSIAN:
            strategy = RussianAlphabetCreationStrategy()
            context = AlphabetCreationContext(strategy)
            return context(uppercase_symbols)

        logger.info("Not Implemented for this alphabet. Please check")

        raise NotImplementedError

    # noinspection PyMethodMayBeStatic
    def get_language_from_the_text(self, text: Text) -> LanguageType:
        if re.fullmatch(r"^[а-яА-ЯЁё][а-яА-ЯЁё\s\-\,\.\:\;\!\?]*[а-яА-ЯЁё]$", str(text), re.UNICODE):
            return LanguageType.RUSSIAN

        if re.fullmatch(r"^[a-zA-Z][a-zA-Z\s\-\,\.\:\;\!\?]*[a-zA-Z]$", str(text), re.UNICODE):
            return LanguageType.ENGLISH

        raise NotImplementedError("Not Implemented for this alphabet.")
