import logging
from collections import deque
from typing import Final, Tuple, List

from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.cipher_table.services.cipher_table_service import CipherTableService
from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.common.values.languages import LanguageType
from cryptography_methods.domain.common.values.text import Text

logger: Final[logging.Logger] = logging.getLogger(__name__)


class PlayfairService(DomainService):
    DEFAULT_FILLER: Final[str] = "Х"

    def __init__(
            self,
            table_service: CipherTableService,
            alphabet_service: AlphabetService,
    ) -> None:
        super().__init__()
        self._table_service: Final[CipherTableService] = table_service
        self._alphabet_service: Final[AlphabetService] = alphabet_service

    def encrypt(
            self,
            table_width: TableDimension,
            table_height: TableDimension,
            keyword: Text,
            text_for_encryption: Text
    ) -> Text:
        return self._process(
            table_width,
            table_height,
            keyword,
            text_for_encryption,
            mode="encrypt"
        )

    def decrypt(
            self,
            table_width: TableDimension,
            table_height: TableDimension,
            keyword: Text,
            text_for_encryption: Text
    ) -> Text:
        return self._process(
            table_width,
            table_height,
            keyword,
            text_for_encryption,
            mode="decrypt"
        )

    def _process(
            self,
            table_width: TableDimension,
            table_height: TableDimension,
            keyword: Text,
            text: Text,
            mode: str
    ) -> Text:
        # Подготовка таблицы
        table = self._build_table(table_width, table_height, keyword, text)
        logger.info("Playfair table created: %s", table.data)

        # Обработка текста
        bigrams = self._prepare_text(text.value)
        logger.info("Prepared bigrams: %s", bigrams)

        # Обработка биграмм
        processed_bigrams = []
        for bigram in bigrams:
            if mode == "encrypt":
                processed = self._encrypt_bigram(table, bigram)
            else:
                processed = self._decrypt_bigram(table, bigram)
            processed_bigrams.append(processed)

        # Сборка результата
        result = self._rebuild_text(text.value, processed_bigrams)
        return Text(result)

    def _build_table(
            self,
            table_width: TableDimension,
            table_height: TableDimension,
            keyword: Text,
            text: Text
    ) -> Table:
        """Создает таблицу Плейфейра"""
        # Определение языка
        language_type = self._alphabet_service.get_language_from_the_text(text)
        alphabet = self._alphabet_service.build_alphabet_by_provided_language_type(
            language_type=language_type,
            uppercase_symbols=True
        )

        # Обработка русского алфавита
        if language_type == LanguageType.RUSSIAN and table_width * table_height == 32:
            alphabet = alphabet.replace("Ё", "")

        # Обработка ключа
        cleaned_keyword = "".join(
            char.upper() for char in keyword.value if char.isalpha()
        )
        unique_key = "".join(dict.fromkeys(cleaned_keyword))
        remaining_alphabet = "".join(char for char in alphabet if char not in unique_key)
        data = unique_key + remaining_alphabet

        # Создание таблицы
        return self._table_service.create(
            width=table_width.value,
            height=table_height.value,
            data=data,
            fill_by_columns=False
        )

    def _prepare_text(self, text: str) -> List[Tuple[str, str]]:
        """Подготавливает текст, разбивая на биграммы"""
        # Фильтрация и нормализация букв
        letters = []
        for char in text:
            if char.isalpha():
                letters.append(char.upper())
            elif char == "Ё":
                letters.append("Е")

        # Формирование биграмм с заполнителем
        bigrams = []
        i = 0
        while i < len(letters):
            # Последняя буква
            if i == len(letters) - 1:
                bigrams.append((letters[i], self.DEFAULT_FILLER))
                break

            # Одинаковые буквы
            if letters[i] == letters[i + 1]:
                bigrams.append((letters[i], self.DEFAULT_FILLER))
                i += 1
            else:
                bigrams.append((letters[i], letters[i + 1]))
                i += 2

        return bigrams

    def _encrypt_bigram(self, table: Table, bigram: Tuple[str, str]) -> Tuple[str, str]:
        """Шифрует биграмму по правилам Плейфейра"""
        char1, char2 = bigram
        row1, col1 = table.find(char1)
        row2, col2 = table.find(char2)

        # Буквы в одной строке
        if row1 == row2:
            new_col1 = (col1 + 1) % table.width
            new_col2 = (col2 + 1) % table.width
            return table[row1, new_col1], table[row2, new_col2]

        # Буквы в одном столбце
        if col1 == col2:
            new_row1 = (row1 + 1) % table.height
            new_row2 = (row2 + 1) % table.height
            return table[new_row1, col1], table[new_row2, col2]

        # Буквы в разных строках и столбцах
        return table[row1, col2], table[row2, col1]

    def _decrypt_bigram(self, table: Table, bigram: Tuple[str, str]) -> Tuple[str, str]:
        """Дешифрует биграмму по правилам Плейфейра"""
        char1, char2 = bigram
        row1, col1 = table.find(char1)
        row2, col2 = table.find(char2)

        # Буквы в одной строке
        if row1 == row2:
            new_col1 = (col1 - 1) % table.width
            new_col2 = (col2 - 1) % table.width
            return table[row1, new_col1], table[row2, new_col2]

        # Буквы в одном столбце
        if col1 == col2:
            new_row1 = (row1 - 1) % table.height
            new_row2 = (row2 - 1) % table.height
            return table[new_row1, col1], table[new_row2, col2]

        # Буквы в разных строках и столбцах
        return table[row1, col2], table[row2, col1]

    def _rebuild_text(self, original: str, bigrams: List[Tuple[str, str]]) -> str:
        """Собирает текст из биграмм с сохранением не-буквенных символов"""
        # Создаем очередь всех букв
        all_chars = deque()
        for a, b in bigrams:
            all_chars.append(a)
            all_chars.append(b)

        # Собираем результат с сохранением оригинального регистра и символов
        result = []
        for char in original:
            if not char.isalpha():
                result.append(char)
                continue

            # Восстановление регистра
            encrypted_char = all_chars.popleft()
            result.append(encrypted_char if char.isupper() else encrypted_char.lower())

        return "".join(result)