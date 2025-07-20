import logging
from typing import Final, overload

from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.cipher_table.errors import (
    TableWidthAndHeightNotDoesntMatchDataError,
    UnknownTypeDataForCreateTableError,
    DataCantContainBadSymbolsError
)
from cryptography_methods.domain.cipher_table.events import TableCreatedAndFilledSuccessfullyEvent
from cryptography_methods.domain.cipher_table.services.id_generator import CipherTableIdGenerator
from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension
from cryptography_methods.domain.common.services import DomainService

logger: Final[logging.Logger] = logging.getLogger(__name__)


class CipherTableService(DomainService):
    def __init__(
            self,
            id_generator: CipherTableIdGenerator
    ) -> None:
        super().__init__()
        self._id_generator: Final[CipherTableIdGenerator] = id_generator

    @overload
    def create(
            self,
            width: int,
            height: int,
            data: str,
            fill_by_columns: bool = False,
    ) -> Table:
        ...

    @overload
    def create(
            self,
            width: int,
            height: int,
            data: list[list[str]],
            fill_by_columns: bool = False
    ) -> Table:
        ...

    def create(
            self,
            width: int,
            height: int,
            data: list[list[str]] | str,
            fill_by_columns: bool = False,
    ) -> Table:
        """
        Метод сервиса, который создает таблицу для шифрования.
        Пробелы в шифртексте обозначаются символом «_», несколько подряд идущих пробелов разделяются символом «|».

        Args:
            width: ширина таблицы (положительное число)
            height: высота таблицы (положительное число)
            data: данные для заполнения в таблицу.
            fill_by_columns: порядок для записи в таблицу из данных. По умолчанию заполнение по строчкам.

        Если data - список, то он уже должен быть обработан по правилу, как сказано в задании.
        В ином случае бросается ошибка.

        Returns: созданный объект таблицы для дальнейшей манипуляции с ним.
        """
        validated_width: TableDimension = TableDimension(width)
        validated_height: TableDimension = TableDimension(height)

        logger.info("Validated width: %s", validated_width)
        logger.info("Validated height: %s", validated_height)

        if (
                isinstance(data, list) and
                all(isinstance(item, list) for item in data) and
                all(isinstance(subitem, str) for sublist in data for subitem in sublist)
        ):
            if any(cell.isspace() or cell == "" for row in data for cell in row):
                raise DataCantContainBadSymbolsError(
                    "В строке не может быть пробелов. Замените пробел на '_' и двойные пробелы на '|'"
                )

            count_of_table_columns_with_data: int = len(data)
            count_of_table_rows_with_data: int = sum(len(row) for row in data)

            logger.info(
                "Count of table columns: %s",
                count_of_table_columns_with_data,
            )
            logger.info(
                "Count of table rows: %s",
                count_of_table_rows_with_data,
            )

            if count_of_table_columns_with_data * count_of_table_rows_with_data != validated_width * validated_height:
                raise TableWidthAndHeightNotDoesntMatchDataError(
                    "Количество данных и фактические размеры таблицы не совпадают"
                )

            filled_table: Table = self.__create_and_fill_data_for_table(
                width=validated_width,
                height=validated_height,
                data=data,
                fill_by_columns=fill_by_columns,
            )

        elif isinstance(data, str):
            if data.isspace() or data == "":
                raise DataCantContainBadSymbolsError("Данные для таблицы не могут быть пустыми")

            if len(data) != validated_width * validated_height:
                raise TableWidthAndHeightNotDoesntMatchDataError(
                    "Количество данных и фактические размеры таблицы не совпадают"
                )

            data_for_creating_table: list[list[str]] = [
                list(data[i * validated_width: (i + 1) * validated_width])
                for i in range(validated_height)
            ]

            filled_table: Table = self.__create_and_fill_data_for_table(
                width=validated_width,
                height=validated_height,
                data=data_for_creating_table,
                fill_by_columns=fill_by_columns,
            )
        else:
            raise UnknownTypeDataForCreateTableError("Неизвестный тип данных для создания таблицы")

        self._record_event(
            TableCreatedAndFilledSuccessfullyEvent(
                table=filled_table,
                fill_by_column=fill_by_columns,
            )
        )

        return filled_table

    def __create_and_fill_data_for_table(
            self,
            width: TableDimension,
            height: TableDimension,
            data: list[list[str]],
            fill_by_columns: bool = False
    ) -> Table:
        created_table: Table = Table(
            id=self._id_generator(),
            width=width,
            height=height
        )

        logger.info("Created empty table: %s", created_table)

        if fill_by_columns:
            logger.info("Filling table by columns")
            # Обработка заполнения по столбцам
            for col in range(width.value):
                for row in range(height.value):
                    created_table[row, col] = data[row][col]
        else:
            logger.info("Filling table by rows")
            # Обработка заполнения по строкам (по умолчанию)
            for row in range(height.value):
                for col in range(width.value):
                    created_table[row, col] = data[row][col]

        for row_index, row in enumerate(data):
            for cell_index, cell in enumerate(row):
                created_table[row_index, cell_index] = cell

        return created_table
