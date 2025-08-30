import logging
from collections import deque
from typing import Final

from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.cipher_table.services.cipher_table_service import CipherTableService
from cryptography_methods.domain.cipher_table.services.id_generator import CipherTableIdGenerator
from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension
from cryptography_methods.domain.common.services.alphabet_service import AlphabetService
from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.common.values.text import Text

logger: Final[logging.Logger] = logging.getLogger(__name__)


class SingleKeyPermutationService(DomainService):
    def __init__(
            self,
            cipher_table_service: CipherTableService,
            table_id_generator: CipherTableIdGenerator,
            alphabet_service: AlphabetService,
    ) -> None:
        super().__init__()
        self._cipher_table_service: Final[CipherTableService] = cipher_table_service
        self._table_id_generator: Final[CipherTableIdGenerator] = table_id_generator
        self._alphabet_service: Final[AlphabetService] = alphabet_service

    def encrypt(self, data: Text, key: Text, width: TableDimension, height: TableDimension) -> Text:
        alphabet: str = self._alphabet_service.build_alphabet_by_provided_text(
            key,
            uppercase_symbols=key.isupper(),
        )

        logger.info("alphabet: %s", alphabet)

        table_with_keys_and_numbers: Table = Table(
            id=self._table_id_generator(),
            width=TableDimension(len(key)),
            height=TableDimension(2)
        )

        logger.info("Created empty table for key and numbers")

        letters: list[str] = list(key)
        logger.info("Letters from key: %s", letters)
        pairs: list[tuple[str, int]] = [(letter, idx) for idx, letter in enumerate(letters, start=0)]
        logger.info("Letters with numbers without sorting: %s", pairs)
        pairs.sort(key=lambda pair: (alphabet.index(pair[0].upper()), pair[1]))
        logger.info("Sorted pairs: %s", pairs)

        res_numbers: list[int] = [0] * len(letters)
        logger.info("Started building numbers for letters in key: %s", res_numbers)
        for order, (_, orig_idx) in enumerate(pairs, start=1):
            res_numbers[orig_idx] = order
            logger.info("res_numbers[%s] = %s", order, res_numbers)

        for col, letter in enumerate(letters):
            table_with_keys_and_numbers[0, col] = letter
        for col, num in enumerate(res_numbers):
            table_with_keys_and_numbers[1, col] = str(num)

        logger.info("Filled data for table with key and numbers\n%s\n", table_with_keys_and_numbers)

        table_with_filled_data_with_text_for_encryption: Table = self._cipher_table_service.create(
            width=width.value,
            height=height.value,
            data=data.value,
            fill_by_columns=True
        )

        stacked_table: Table = self._cipher_table_service.vertical_stack(
            upper_table=table_with_keys_and_numbers,
            lower_table=table_with_filled_data_with_text_for_encryption,
        )

        sorted_stacked_table: Table = self._cipher_table_service.sort_columns_by_row(
            stacked_table,
            row_index=1
        )

        cipher_parts: deque[str] = deque()
        row: list[str]

        for row_idx in range(2, sorted_stacked_table.height):
            row: list[str] = sorted_stacked_table[row_idx]
            cipher_parts.append("".join(row))

        return Text("".join(cipher_parts))


    def decrypt(self, data: Text, key: Text, width: TableDimension, height: TableDimension) -> Text:
        alphabet: str = self._alphabet_service.build_alphabet_by_provided_text(
            key,
            uppercase_symbols=key.isupper(),
        )

        logger.info("alphabet: %s", alphabet)

        table_with_keys_and_numbers: Table = Table(
            id=self._table_id_generator(),
            width=TableDimension(len(key)),
            height=TableDimension(2)
        )

        logger.info("Created empty table for key and numbers")

        letters: list[str] = list(key)
        logger.info("Letters from key: %s", letters)

        # Создаем пары (буква, индекс) и сортируем по алфавиту
        pairs: list[tuple[str, int]] = [(letter, idx) for idx, letter in enumerate(letters)]
        logger.info("Letters with numbers without sorting: %s", pairs)
        pairs.sort(key=lambda pair: (alphabet.index(pair[0].upper()), pair[1]))
        logger.info("Sorted pairs: %s", pairs)

        # Вычисляем порядковые номера для букв ключа
        res_numbers: list[int] = [0] * len(letters)
        for order, (_, orig_idx) in enumerate(pairs, start=1):
            res_numbers[orig_idx] = order

        # Заполняем таблицу ключа и номеров
        sorted_letters: list[str] = [letter for letter, _ in pairs]  # Буквы в отсортированном порядке
        for col, letter in enumerate(sorted_letters):
            table_with_keys_and_numbers[0, col] = letter
        for col, num in enumerate(range(1, len(letters) + 1)):
            table_with_keys_and_numbers[1, col] = str(num)

        logger.info("Filled data for table with key and numbers\n%s\n", table_with_keys_and_numbers)

        # Создаем таблицу с зашифрованными данными
        table_with_encrypted_data: Table = self._cipher_table_service.create(
            width=width.value,
            height=height.value,
            data=data.value,
            fill_by_columns=False  # Заполняем по строкам, так как данные пришли в виде строк
        )

        # Объединяем таблицы
        stacked_table: Table = self._cipher_table_service.vertical_stack(
            upper_table=table_with_keys_and_numbers,
            lower_table=table_with_encrypted_data,
        )

        logger.info("Stacked table before sorting:\n%s\n", stacked_table)

        # Вычисляем обратную перестановку для восстановления исходного порядка
        # Создаем mapping: номер -> позиция в отсортированной таблице
        number_to_position: dict[int, int] = {num: idx for idx, num in enumerate(range(1, len(letters) + 1))}

        # Определяем порядок столбцов для восстановления исходной таблицы
        reverse_order: list[int] = [number_to_position[num] for num in res_numbers]
        logger.info("Reverse order for columns: %s", reverse_order)

        # Создаем таблицу с восстановленным порядком столбцов
        restored_table: Table = Table(
            id=self._table_id_generator(),
            width=stacked_table.width,
            height=stacked_table.height
        )

        # Восстанавливаем исходный порядок столбцов
        for col in range(stacked_table.width):
            original_col: int = reverse_order[col]
            for row in range(stacked_table.height):
                restored_table[row, col] = stacked_table[row, original_col]

        logger.info("Restored table:\n%s\n", restored_table)

        # Извлекаем расшифрованные данные (пропускаем первые две строки с ключом)
        decrypted_parts: deque[str] = deque()
        for col in range(restored_table.width):
            for row in range(2, restored_table.height):
                decrypted_parts.append(restored_table[row, col])

        decrypted_text: str = "".join(decrypted_parts)
        decrypted_text: str = decrypted_text.replace("_", " ").replace("|", "  ")

        return Text(decrypted_text)

