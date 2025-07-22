import logging
from typing import Final

from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.cipher_table.errors import (
    TableWidthAndHeightNotDoesntMatchDataError,
    DataCantContainBadSymbolsError,
    TableSizesDoNotMatchError
)
from cryptography_methods.domain.cipher_table.events import TableCreatedAndFilledSuccessfullyEvent
from cryptography_methods.domain.cipher_table.services.id_generator import CipherTableIdGenerator
from cryptography_methods.domain.cipher_table.services.table_creation.base import TableCreationStrategy
from cryptography_methods.domain.cipher_table.services.table_creation.by_columns_strategy import (
    ByColumnsTableCreationStrategy
)
from cryptography_methods.domain.cipher_table.services.table_creation.by_rows_strategy import (
    ByRowsTableCreationStrategy
)
from cryptography_methods.domain.cipher_table.services.table_creation.context import TableCreationContext
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

    def create(
            self,
            width: int,
            height: int,
            data: str,
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

        if data.isspace() or data == "":
            raise DataCantContainBadSymbolsError("The data for the table cannot be empty")

        count_of_symbols: int = len(data)

        logger.info("Length of symbols: %s in sentence", count_of_symbols)

        if count_of_symbols != validated_width * validated_height:
            raise TableWidthAndHeightNotDoesntMatchDataError(
                "The amount of data and the actual size of the table do not match"
            )

        strategy: TableCreationStrategy

        if fill_by_columns:
            strategy = ByColumnsTableCreationStrategy(
                id_generator=self._id_generator,
            )
        else:
            strategy = ByRowsTableCreationStrategy(
                id_generator=self._id_generator,
            )

        context: TableCreationContext = TableCreationContext(
            strategy=strategy,
        )

        table: Table = context(
            data=data,
            width=validated_width,
            height=validated_height,
        )

        self._record_event(
            TableCreatedAndFilledSuccessfullyEvent(
                table=table,
                fill_by_column=fill_by_columns,
            )
        )

        return table

    def vertical_stack(self, upper_table: Table, lower_table: Table) -> Table:
        logger.info("Checking that lower and upper table width matching...")

        if upper_table.width != lower_table.width:
            raise TableSizesDoNotMatchError("width of upper and lower tables do not match")

        stacked_table: Table = Table(
            id=self._id_generator(),
            width=upper_table.width,
            height=upper_table.height + lower_table.height,
        )

        for row_idx in range(upper_table.height):
            stacked_table.data[row_idx] = upper_table[row_idx][:]

        for row_idx in range(lower_table.height):
            stacked_table.data[lower_table.height + row_idx] = lower_table.data[row_idx][:]

        logger.info("Built stacked table using vertical stack, new table:\n%s\n", stacked_table)

        return stacked_table


