from typing import Final

from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.cipher_table.events import SwappedSpacesOnSymbolsEvent
from cryptography_methods.domain.cipher_table.services.cipher_table_service import CipherTableService
from cryptography_methods.domain.common.services.base import DomainService


class SimpleTablePermutationService(DomainService):
    """
    Сервис для реализации логики шифра - простая перестановка.
    """

    def __init__(self, cipher_table_service: CipherTableService) -> None:
        super().__init__()
        self._cipher_table_service: Final[CipherTableService] = cipher_table_service

    def encrypt(self, data: str, width: int, height: int) -> str:
        """
        Метод, который шифрует переданные данные с помощью метода - простая перестановка.
        Здесь логика заключается в том, что передаются данные, заполняются в таблицу в столбец.
        Т.е ваша строчка будет записана не по-привычному в строку, а в столбец именно.

        Args:
            data: Данные для шифрования.
            width: Количество строк таблицы шифрования.
            height: Количество столбцов таблицы шифрования.

        Returns:
            Зашифрованные данные в виде строки с помощью метода простых перестановок.
        """
        mapped_data: str = data.replace("  ", "|").replace(" ", "_")

        self._record_event(
            SwappedSpacesOnSymbolsEvent(
                old_string=data,
                new_string=mapped_data,
            )
        )

        table: Table = self._cipher_table_service.create(
            width=width,
            height=height,
            data=mapped_data,
            fill_by_columns=True
        )

        self._record_events(
            self._cipher_table_service.pull_events()
        )

        return "".join("".join(column for column in row) for row in table)

    def decrypt(self, data: str, width: int, height: int) -> str:
        """
        Метод, который дешифрует переданные данные с помощью метода - простая перестановка.
        Здесь логика заключается в том, что передаются данные, заполняются в таблицу в строку.
        Потом я делаю транспонирование, чтобы считать по строкам.

        Args:
            data: Данные для дешифрования.
            width: ширина таблицы
            height: высота таблицы.

        Returns:
            Возвращает дешифрованное сообщение
        """
        table: Table = self._cipher_table_service.create(
            width=width,
            height=height,
            data=data,
            fill_by_columns=False
        )

        self._record_events(
            self._cipher_table_service.pull_events()
        )

        transposed_data: zip = zip(*table)

        self._record_event(
            ...
        )

        decrypted_string_without_spaces: str = "".join("".join(column for column in row) for row in transposed_data)
        return decrypted_string_without_spaces.replace("|", "  ").replace("_", " ")
