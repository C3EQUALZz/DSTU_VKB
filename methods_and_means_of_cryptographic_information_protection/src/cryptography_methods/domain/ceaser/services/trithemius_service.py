import logging
from collections import deque
from typing import Final

from cryptography_methods.domain.ceaser.errors import TextLanguageAndKeyLanguageAreDifferentError
from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.cipher_table.services.cipher_table_service import CipherTableService
from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.common.values.languages import LanguageType
from cryptography_methods.domain.common.values.text import Text

logger: Final[logging.Logger] = logging.getLogger(__name__)


class TrithemiusService(DomainService):
    def __init__(
            self,
            table_service: CipherTableService,
            alphabet_service: AlphabetService,
    ) -> None:
        self._table_service: Final[CipherTableService] = table_service
        self._alphabet_service: Final[AlphabetService] = alphabet_service

    def encrypt(
            self,
            table_width: TableDimension,
            table_height: TableDimension,
            keyword: Text,
            text_for_encryption: Text
    ) -> Text:
        # Ключ приводим к нижнему регистру (для построения таблицы)
        lowered_keyword: Text = keyword.lower()

        # Уникальные символы ключа (в нижнем регистре)
        unique_symbols_from_key = "".join(dict.fromkeys(lowered_keyword.value))
        logger.info("Got unique symbols from key: %s", unique_symbols_from_key)

        # Определяем язык по оригинальному тексту (с сохранением регистра)
        language_type: LanguageType = self._alphabet_service.get_language_from_the_text(
            text=text_for_encryption
        )
        logger.info("Got language type: %s", language_type)

        # Алфавит строим по оригинальному тексту, но в нижнем регистре
        alphabet_by_text: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=Text(value=text_for_encryption.value.lower()),
        )

        alphabet_by_keyword: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=lowered_keyword,
        )

        if alphabet_by_text != alphabet_by_keyword:
            raise TextLanguageAndKeyLanguageAreDifferentError(
                "The key and text must have the same languages"
            )

        if language_type is LanguageType.RUSSIAN and table_width * table_height == 32:
            alphabet_by_text = "".join(
                alpha for alpha in alphabet_by_text if alpha not in {"ё"}
            )
            logger.info(
                "User provided russian text and table size is 32, removed 'ё', alphabet: %s",
                alphabet_by_text,
            )

        alphabet_without_alphas_from_keyword: str = "".join(
            alpha for alpha in alphabet_by_text
            if alpha not in lowered_keyword.value
        )
        logger.info(
            "Built alphabet without alphas from keyword: %s",
            alphabet_without_alphas_from_keyword
        )

        data_for_table: str = unique_symbols_from_key + alphabet_without_alphas_from_keyword
        logger.info("Data for table: %s", data_for_table)

        table: Table = self._table_service.create(
            width=table_width.value,
            height=table_height.value,
            data=data_for_table,
            fill_by_columns=False
        )

        result: deque[str] = deque()

        # Обрабатываем каждый символ с сохранением регистра
        for char in text_for_encryption.value:
            logger.info("Encrypting char: %s", char)

            # Пропускаем не-буквы
            if char not in alphabet_by_text and char.lower() not in alphabet_by_text:
                result.append(char)
                continue

            # Определяем регистр
            was_upper: bool = char.isupper()
            char_lower: str = char.lower()

            # Ищем позицию в таблице (в нижнем регистре)
            row_index, column_index = table.find(char_lower)

            # Шифруем символ
            encrypted_char: str = table[(row_index + 1) % table.height, column_index]

            # Восстанавливаем регистр
            if was_upper:
                encrypted_char = encrypted_char.upper()

            result.append(encrypted_char)

        return Text("".join(result))

    def decrypt(
            self,
            table_width: TableDimension,
            table_height: TableDimension,
            keyword: Text,
            text_for_decryption: Text
    ) -> Text:
        lowered_keyword: Text = keyword.lower()
        unique_symbols_from_key = "".join(dict.fromkeys(lowered_keyword.value))

        logger.info("Got unique symbols from key: %s", unique_symbols_from_key)

        # Определяем язык по оригинальному тексту (с сохранением регистра)
        language_type: LanguageType = self._alphabet_service.get_language_from_the_text(
            text=text_for_decryption
        )
        logger.info("Got language type: %s", language_type)

        # Алфавит строим по оригинальному тексту, но в нижнем регистре
        alphabet_by_text: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=Text(value=text_for_decryption.value.lower()),
        )

        alphabet_by_keyword: str = self._alphabet_service.build_alphabet_by_provided_text(
            text=lowered_keyword,
        )

        if alphabet_by_text != alphabet_by_keyword:
            raise TextLanguageAndKeyLanguageAreDifferentError(
                "The key and text must have the same languages"
            )

        if language_type is LanguageType.RUSSIAN and table_width * table_height == 32:
            alphabet_by_text = "".join(
                alpha for alpha in alphabet_by_text if alpha not in {"ё"}
            )
            logger.info(
                "User provided russian text and table size is 32, removed 'ё', alphabet: %s",
                alphabet_by_text,
            )

        alphabet_without_alphas_from_keyword: str = "".join(
            alpha for alpha in alphabet_by_text
            if alpha not in lowered_keyword.value
        )
        logger.info(
            "Built alphabet without alphas from keyword: %s",
            alphabet_without_alphas_from_keyword
        )

        data_for_table: str = unique_symbols_from_key + alphabet_without_alphas_from_keyword
        logger.info("Data for table: %s", data_for_table)

        table: Table = self._table_service.create(
            width=table_width.value,
            height=table_height.value,
            data=data_for_table,
            fill_by_columns=False
        )

        result: deque[str] = deque()

        for char in text_for_decryption.value:
            logger.info("Decrypting char: %s", char)

            if char not in alphabet_by_text and char.lower() not in alphabet_by_text:
                result.append(char)
                continue

            was_upper: bool = char.isupper()
            char_lower: str = char.lower()

            row_index, column_index = table.find(char_lower)
            decrypted_char: str = table[(row_index - 1) % table.height, column_index]

            if was_upper:
                decrypted_char = decrypted_char.upper()

            result.append(decrypted_char)

        return Text("".join(result))
