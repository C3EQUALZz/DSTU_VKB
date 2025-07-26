from itertools import cycle
import logging
from collections import deque
from typing import Final

from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.common.values.text import Text

logger: Final[logging.Logger] = logging.getLogger(__name__)


class VigenereService(DomainService):
    def __init__(self, alphabet_service: AlphabetService) -> None:
        super().__init__()
        self._alphabet_service: Final[AlphabetService] = alphabet_service

    def encrypt(self, key: Text, text: Text) -> Text:
        return self._transform(key, text, is_encrypt=True)

    def decrypt(self, key: Text, text: Text) -> Text:
        return self._transform(key, text, is_encrypt=False)

    def _transform(self, key: Text, text: Text, is_encrypt: bool) -> Text:
        alphabet: str = self._alphabet_service.build_alphabet_by_provided_text(
            text,
            uppercase_symbols=True
        )
        logger.info("Using alphabet: %s (length: %d)", alphabet, len(alphabet))

        # Оптимизированная очистка ключа с использованием set для быстрого поиска
        alphabet_set: set[str] = set(alphabet)
        cleaned_key: str = ''.join(filter(alphabet_set.__contains__, key.value.upper()))

        # Создаем бесконечный итератор ключа
        key_iter: cycle[str] = cycle(cleaned_key)
        n: int = len(alphabet)

        # Используем deque для эффективного добавления символов
        result_chars: deque[str] = deque()
        # Создаем словарь для быстрого поиска индексов символов
        char_index_map: dict[str, int] = {char: idx for idx, char in enumerate(alphabet)}

        for char in text.value:
            char_upper = char.upper()
            if char_upper in char_index_map:
                key_char: str = next(key_iter)
                logger.info("Key char for encryption: %s", key_char)

                text_pos: int = char_index_map[char_upper]
                key_pos: int = char_index_map[key_char]

                logger.info("Text index: %s, key position: %s", text_pos, key_pos)

                # Применяем преобразование Виженера
                offset: int = key_pos if is_encrypt else -key_pos
                logger.info("Offset for encryption: %s", offset)

                new_pos: int = (text_pos + offset) % n
                logger.info("New position for encryption: %s", new_pos)

                new_char: str = alphabet[new_pos]
                new_char_for_encryption: str = new_char if char.isupper() else new_char.lower()
                logger.info("New char for encryption: %s", new_char_for_encryption)

                # Добавляем символ с сохранением регистра
                result_chars.append(new_char_for_encryption)
            else:
                result_chars.append(char)

        return Text(''.join(result_chars))
