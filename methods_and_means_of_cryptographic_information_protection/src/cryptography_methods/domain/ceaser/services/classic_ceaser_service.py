import logging
from typing import Final, Mapping

from cryptography_methods.domain.ceaser.values.key_classic_caesar import KeyClassicCaesar
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.common.values.languages import LanguageType
from cryptography_methods.domain.common.values.text import Text

logger: Final[logging.Logger] = logging.getLogger(__name__)


class ClassicCeaserService(DomainService):
    def __init__(
            self,
            alphabet_service: AlphabetService
    ) -> None:
        super().__init__()
        self._alphabet_service: Final[AlphabetService] = alphabet_service

    def encrypt(self, key: KeyClassicCaesar, text: Text) -> str:
        logger.info("Started encryption using Classic Ceaser...")

        language_type: LanguageType = self._alphabet_service.get_language_from_the_text(
            text
        )
        logger.info("Got language type: %s", language_type)

        translation_dictionary: Mapping[int, int] = self.__build_translation_dictionary(
            language_type=language_type,
            key=key
        )

        encrypted_text: str = str.translate(str(text), translation_dictionary)
        logger.info("Encrypted text: %s", encrypted_text)
        return encrypted_text

    def decrypt(self, key: KeyClassicCaesar, text: Text) -> str:
        language_type: LanguageType = self._alphabet_service.get_language_from_the_text(
            text
        )

        translation_dictionary: Mapping[int, int] = {
            v: k for k, v in self.__build_translation_dictionary(
                language_type=language_type,
                key=key
            ).items()
        }

        logger.info(
            "Swapped values and keys for translation dictionary: %s",
            {chr(k): chr(v) for k, v in translation_dictionary.items()}
        )

        decrypted_text: str = str.translate(str(text), translation_dictionary)

        logger.info("Got decrypted text: %s", decrypted_text)

        return decrypted_text

    def __build_translation_dictionary(
            self,
            language_type: LanguageType,
            key: KeyClassicCaesar
    ) -> Mapping[int, int]:
        lowercase_alphabet: str = self._alphabet_service.build_alphabet_by_provided_language_type(
            language_type,
            uppercase_symbols=False
        )

        uppercase_alphabet: str = self._alphabet_service.build_alphabet_by_provided_language_type(
            language_type,
            uppercase_symbols=True
        )

        translation_dictionary: Mapping[int, int] = str.maketrans(
            lowercase_alphabet,
            lowercase_alphabet[key:]
            + lowercase_alphabet[:key],
        ) | str.maketrans(
            uppercase_alphabet,
            uppercase_alphabet[key:]
            + uppercase_alphabet[:key],
        )

        logger.info(
            "Built translation dictionary: %s",
            {chr(k): chr(v) for k, v in translation_dictionary.items()}
        )

        return translation_dictionary
