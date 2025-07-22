import logging
import re
from typing import Final

from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.cipher_table.services.alphabet_creation.base import AlphabetCreationStrategy
from cryptography_methods.domain.cipher_table.services.alphabet_creation.context import AlphabetCreationContext
from cryptography_methods.domain.cipher_table.services.alphabet_creation.english_strategy import (
    EnglishAlphabetCreationStrategy
)
from cryptography_methods.domain.cipher_table.services.alphabet_creation.russian_strategy import (
    RussianAlphabetCreationStrategy
)
from cryptography_methods.domain.cipher_table.services.cipher_table_service import CipherTableService
from cryptography_methods.domain.cipher_table.services.id_generator import CipherTableIdGenerator
from cryptography_methods.domain.cipher_table.values.key_simple_key_permutation import KeyForSimpleKeyPermutation
from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension
from cryptography_methods.domain.common.services.base import DomainService
from collections import deque

logger: Final[logging.Logger] = logging.getLogger(__name__)


class SingleKeyPermutationService(DomainService):
    def __init__(
            self,
            cipher_table_service: CipherTableService,
            table_id_generator: CipherTableIdGenerator
    ) -> None:
        super().__init__()
        self._cipher_table_service: Final[CipherTableService] = cipher_table_service
        self._table_id_generator: Final[CipherTableIdGenerator] = table_id_generator

    def encrypt(self, data: str, key: str, width: int, height: int) -> str:
        mapped_data: str = data.replace("  ", "|").replace(" ", "_")
        logger.info("Replaced all spaces on symbols in text for encryption, changed data: %s", mapped_data)
        mapped_key: str = key.replace("  ", "|").replace(" ", "_")
        logger.info("Replace all spaces on symbols in key for encryption, changed data: %s", mapped_key)

        logger.info("Validating key")

        validated_key: KeyForSimpleKeyPermutation = KeyForSimpleKeyPermutation(
            value=mapped_key,
        )

        alphabet: str = self.__build_alphabet_by_key(validated_key)

        table_with_keys_and_numbers: Table = Table(
            id=self._table_id_generator(),
            width=TableDimension(len(mapped_key)),
            height=TableDimension(2)
        )

        logger.info("Created empty table for key and numbers")

        letters: list[str] = list(validated_key.value)
        pairs: list[tuple[str, int]] = [(letter, idx) for idx, letter in enumerate(letters)]
        pairs.sort(key=lambda pair: (alphabet.index(pair[0].upper()), pair[1]))

        res_numbers: list[int] = [0] * len(letters)
        for order, (_, orig_idx) in enumerate(pairs, start=1):
            res_numbers[orig_idx] = order

        for col, letter in enumerate(letters):
            table_with_keys_and_numbers[0, col] = letter
        for col, num in enumerate(res_numbers):
            table_with_keys_and_numbers[1, col] = str(num)

        logger.info("Filled data for table with key and numbers\n%s\n", table_with_keys_and_numbers)

        table_with_filled_data_with_text_for_encryption: Table = self._cipher_table_service.create(
            width=width,
            height=height,
            data=data
        )

        stacked_table: Table = self._cipher_table_service.vertical_stack(
            upper_table=table_with_keys_and_numbers,
            lower_table=table_with_filled_data_with_text_for_encryption,
        )

        cipher_parts: deque[str] = deque()
        row: list[str]

        for row_idx in range(2, stacked_table.height):
            row = stacked_table[row_idx]
            cipher_parts.append("".join(row))

        return "".join(cipher_parts)


    def decrypt(self, data: str, key: str, width: int, height: int) -> str:
        mapped_data: str = data.replace("  ", "|").replace(" ", "_")
        mapped_key: str = key.replace("  ", "|").replace(" ", "_")
        return ""

    def __build_alphabet_by_key(self, key: KeyForSimpleKeyPermutation) -> str:
        logger.info("Building alphabet by key letters")
        strategy: AlphabetCreationStrategy
        context: AlphabetCreationContext

        if re.fullmatch(r"^[a-zA-Z]+$", key.value):
            strategy = EnglishAlphabetCreationStrategy()
            context = AlphabetCreationContext(strategy)
            return context()

        if re.fullmatch(r"^[а-яА-Я]+$", key.value):
            strategy = RussianAlphabetCreationStrategy()
            context = AlphabetCreationContext(strategy)
            return context()

        logger.info("Not Implemented for this alphabet. Please check")

        raise NotImplementedError

    def __reorder_columns_by_second_row(self, table: Table) -> Table:
        if table.height < 2:
            return table

        order_row: list[str] = table[1]

        try:
            order_values: list[int] = [int(x) for x in order_row]
        except ValueError as e:
            logger.error("Invalid order values: %s", order_row)
            raise ValueError("Order row must contain integers") from e

        # Создаем новую таблицу для результата
        reordered_table: Table = Table(
            id=self._table_id_generator(),
            width=table.width,
            height=table.height
        )

        # Определяем порядок сортировки столбцов
        sorted_indices = sorted(
            range(len(order_values)),
            key=lambda i: order_values[i]
        )

        for row_idx in range(table.height):
            new_row = [table[row_idx, col_idx] for col_idx in sorted_indices]
            reordered_table[row_idx] = new_row

        return reordered_table

