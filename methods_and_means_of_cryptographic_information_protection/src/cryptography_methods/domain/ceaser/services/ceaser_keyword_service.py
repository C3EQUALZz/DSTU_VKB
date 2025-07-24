import logging
from collections import deque
from typing import Final

from cryptography_methods.domain.ceaser.errors import TextLanguageAndKeyLanguageAreDifferentError
from cryptography_methods.domain.ceaser.values.key_ceaser_keyword import KeyCeaserKeyword
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.common.values.text import Text

logger: Final[logging.Logger] = logging.getLogger(__name__)


class CeaserKeywordService(DomainService):
    def __init__(self, alphabet_service: AlphabetService) -> None:
        super().__init__()
        self._alphabet_service: Final[AlphabetService] = alphabet_service

    def encrypt(self, key: KeyCeaserKeyword, text: Text) -> Text:
        logger.info("Started encryption for %s using Ceaser keyword algorithm", str(text))

        keyword_with_distinct_symbols: str = ''.join(dict.fromkeys(key.keyword))

        alphabet: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=text
        )

        alphabet_for_key: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=Text(value=keyword_with_distinct_symbols)
        )

        if alphabet != alphabet_for_key:
            raise TextLanguageAndKeyLanguageAreDifferentError(
                f"text and key languages are different"
            )

        alphabet_without_alphas_from_key: str = ''.join(
            alpha for alpha in alphabet if alpha not in keyword_with_distinct_symbols.lower()
        )

        logger.info(
            "Built alphabet without key values: %s",
            alphabet_without_alphas_from_key
        )

        step: int = key.k

        first_half_of_alphabet: str = alphabet_without_alphas_from_key[-step:]
        logger.info("First half of new alphabet: %s", first_half_of_alphabet)
        middle_part_of_alphabet: str = keyword_with_distinct_symbols.lower()
        logger.info("Middle part of new alphabet: %s", middle_part_of_alphabet)
        last_part_of_alphabet: str = alphabet_without_alphas_from_key[:-step]
        logger.info("Last part of new alphabet: %s", last_part_of_alphabet)

        new_alphabet_for_encryption: str = first_half_of_alphabet + middle_part_of_alphabet + last_part_of_alphabet
        logger.info("New alphabet after encryption: %s", new_alphabet_for_encryption)

        # Создаем словарь для замены (только нижний регистр)
        translation_dict: dict[str, str] = {}
        for orig_char, new_char in zip(alphabet, new_alphabet_for_encryption):
            translation_dict[orig_char] = new_char

        logger.info(
            "Built translation dictionary from old alphabet to new: %s",
            translation_dict
        )

        # Обрабатываем каждый символ с сохранением регистра
        result_chars: deque[str] = deque()
        for char in text.value:
            if char.lower() in translation_dict:
                replacement = translation_dict[char.lower()]
                # Восстанавливаем оригинальный регистр
                result_chars.append(replacement.upper() if char.isupper() else replacement)
            else:
                result_chars.append(char)

        return Text(''.join(result_chars))

    def decrypt(self, key: KeyCeaserKeyword, text: Text) -> Text:
        logger.info("Started decryption for %s using Ceaser keyword algorithm", str(text))

        alphabet: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=text
        )

        keyword_with_distinct_symbols: str = ''.join(dict.fromkeys(key.keyword))
        unique_keyword_symbols_lowercase: str = keyword_with_distinct_symbols.lower()

        alphabet_without_alphas_from_key: str = ''.join(
            alpha for alpha in alphabet if alpha not in unique_keyword_symbols_lowercase
        )

        logger.info(
            "Built alphabet without key values: %s",
            alphabet_without_alphas_from_key
        )

        step: int = key.k

        first_half_of_alphabet: str = alphabet_without_alphas_from_key[-step:]
        logger.info("First half of new alphabet: %s", first_half_of_alphabet)
        middle_part_of_alphabet: str = unique_keyword_symbols_lowercase
        logger.info("Middle part of new alphabet: %s", middle_part_of_alphabet)
        last_part_of_alphabet: str = alphabet_without_alphas_from_key[:-step]
        logger.info("Last part of new alphabet: %s", last_part_of_alphabet)

        new_alphabet_for_decryption: str = first_half_of_alphabet + middle_part_of_alphabet + last_part_of_alphabet
        logger.info("New alphabet after decryption: %s", new_alphabet_for_decryption)

        # Создаем словарь для замены (только нижний регистр)
        translation_dict: dict[str, str] = {}
        for new_char, orig_char in zip(new_alphabet_for_decryption, alphabet):
            translation_dict[new_char] = orig_char

        logger.info(
            "Built translation dictionary from new alphabet to old: %s",
            translation_dict
        )

        # Обрабатываем каждый символ с сохранением регистра
        result_chars: deque[str] = deque()
        for char in text.value:
            if char.lower() in translation_dict:
                replacement = translation_dict[char.lower()]
                # Восстанавливаем оригинальный регистр
                result_chars.append(replacement.upper() if char.isupper() else replacement)
            else:
                result_chars.append(char)

        return Text(''.join(result_chars))