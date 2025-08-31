import logging
import random
from typing import Final

from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.cipher_table.services.cipher_table_service import CipherTableService
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.common.values.languages import LanguageType
from cryptography_methods.domain.common.values.text import Text
from cryptography_methods.domain.double_square_whitestone.entities.double_table import DoubleTableWhitestone
from cryptography_methods.domain.double_square_whitestone.errors import UnSupportedLanguageTypeForThisCypher
from cryptography_methods.domain.double_square_whitestone.services.id_generator import DoubleTableWhitestoneIdGenerator

logger: Final[logging.Logger] = logging.getLogger(__name__)


class DoubleSquareWhitestoneService(DomainService):
    def __init__(
            self,
            alphabet_service: AlphabetService,
            table_service: CipherTableService,
            id_generator: DoubleTableWhitestoneIdGenerator
    ) -> None:
        super().__init__()
        self._alphabet_service: Final[AlphabetService] = alphabet_service
        self._table_service: Final[CipherTableService] = table_service
        self._id_generator: Final[DoubleTableWhitestoneIdGenerator] = id_generator

    def create_with_tables(self, left_table: Table, right_table: Table) -> DoubleTableWhitestone:
        return DoubleTableWhitestone(
            id=self._id_generator(),
            left_table=left_table,
            right_table=right_table,
        )

    def create(self, width: int = 5, height: int = 7) -> DoubleTableWhitestone:
        russian_alphabet_symbols: str = self._alphabet_service.build_alphabet_by_provided_language_type(
            LanguageType.RUSSIAN,
            uppercase_symbols=True,
        )

        russian_symbols_with_punctation: str = russian_alphabet_symbols + ", .:"
        shuffled_for_first_table: str = "".join(
            random.sample(
                russian_symbols_with_punctation,
                len(russian_symbols_with_punctation)
            )
        )

        shuffled_for_second_table: str = "".join(
            random.sample(
                shuffled_for_first_table,
                len(shuffled_for_first_table)
            )
        )

        first_table: Table = self._table_service.create(
            width=width,
            height=height,
            data=shuffled_for_first_table,
        )

        second_table: Table = self._table_service.create(
            width=width,
            height=height,
            data=shuffled_for_second_table
        )

        return DoubleTableWhitestone(
            id=self._id_generator(),
            left_table=first_table,
            right_table=second_table,
        )

    def encrypt(self, text: Text, key_for_encryption: DoubleTableWhitestone) -> Text:
        language_type: LanguageType = self._alphabet_service.get_language_from_the_text(text)

        if language_type != LanguageType.RUSSIAN:
            raise UnSupportedLanguageTypeForThisCypher("Please give a Russian text for encryption.")

        encrypted_text: str = ''
        raw_text: str = text.value
        first_char: str
        second_char: str
        first_char_row_index: int
        first_char_column_index: int
        second_char_row_index: int
        second_char_column_index: int

        for i in range(0, len(raw_text), 2):
            first_char = raw_text[i]
            second_char = raw_text[i + 1]
            logger.info("Processing pair: (%s, %s)", first_char, second_char)
            first_char_row_index, first_char_column_index = key_for_encryption.left_table.find(first_char)
            logger.info(
                "Indexes for first char in left table: row - %s, column - %s",
                first_char_row_index,
                first_char_column_index
            )
            second_char_row_index, second_char_column_index = key_for_encryption.right_table.find(second_char)
            logger.info(
                "Indexes for second char in right table: row - %s, column - %s",
                second_char_row_index,
                second_char_column_index
            )

            if first_char_row_index == second_char_row_index:  # Одна строка
                logger.info("Chars in same row")
                encrypted_text += key_for_encryption.right_table[first_char_row_index][first_char_column_index]
                logger.info(
                    "Taking new encrypted char at indexes in right table: row - %s, column - %s, encrypted char - %s",
                    first_char_row_index,
                    first_char_column_index,
                    key_for_encryption.right_table[first_char_row_index][first_char_column_index]
                )
                encrypted_text += key_for_encryption.left_table[second_char_row_index][second_char_column_index]
                logger.info(
                    "Taking new encrypted char in left table: row - %s, column - %s, encrypted char - %s",
                    second_char_row_index,
                    second_char_column_index,
                    key_for_encryption.left_table[second_char_row_index][second_char_column_index]
                )
            elif first_char_column_index == second_char_column_index:  # Один столбец
                logger.info("Chars in same column")
                encrypted_text += key_for_encryption.right_table[first_char_row_index][first_char_column_index]
                logger.info(
                    "Taking new encrypted char in right table: row - %s, column - %s",
                    first_char_row_index,
                    first_char_column_index
                )
                encrypted_text += key_for_encryption.left_table[second_char_row_index][second_char_column_index]
            else:
                encrypted_text += key_for_encryption.right_table[first_char_row_index][second_char_column_index]
                encrypted_text += key_for_encryption.left_table[second_char_row_index][first_char_column_index]

            logger.info("Encrypted text: %s", encrypted_text)

        return Text(encrypted_text)

    def decrypt(self, text: Text, key_for_encryption: DoubleTableWhitestone) -> Text:
        language_type: LanguageType = self._alphabet_service.get_language_from_the_text(text)

        if language_type != LanguageType.RUSSIAN:
            raise UnSupportedLanguageTypeForThisCypher("Please give a Russian text for decryption.")

        decrypted_text = ''
        raw_text: str = text.value
        first_char: str
        second_char: str
        first_char_row_index: int
        first_char_column_index: int
        second_char_row_index: int
        second_char_column_index: int

        for i in range(0, len(raw_text), 2):
            first_char = raw_text[i]
            second_char = raw_text[i + 1]
            first_char_row_index, first_char_column_index = key_for_encryption.right_table.find(first_char)
            second_char_row_index, second_char_column_index = key_for_encryption.left_table.find(second_char)

            if first_char_row_index == second_char_row_index:  # Одна строка
                decrypted_text += key_for_encryption.left_table[first_char_row_index][first_char_column_index]
                decrypted_text += key_for_encryption.right_table[second_char_row_index][second_char_column_index]
            elif first_char_column_index == second_char_column_index:  # Один столбец
                decrypted_text += key_for_encryption.left_table[first_char_row_index][first_char_column_index]
                decrypted_text += key_for_encryption.right_table[second_char_row_index][second_char_column_index]
            else:
                decrypted_text += key_for_encryption.left_table[first_char_row_index][second_char_column_index]
                decrypted_text += key_for_encryption.right_table[second_char_row_index][first_char_column_index]
        return decrypted_text
