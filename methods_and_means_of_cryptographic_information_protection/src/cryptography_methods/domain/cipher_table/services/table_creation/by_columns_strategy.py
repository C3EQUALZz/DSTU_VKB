import logging
from typing import Final
from typing_extensions import override

from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.cipher_table.services.table_creation.base import TableCreationStrategy
from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension

logger: Final[logging.Logger] = logging.getLogger(__name__)


class ByColumnsTableCreationStrategy(TableCreationStrategy):
    @override
    def create_table(
            self,
            data: str,
            width: TableDimension,
            height: TableDimension
    ) -> Table:
        logger.info("Creating table by column strategy")

        table: Table = Table(
            id=self._id_generator(),
            width=width,
            height=height
        )

        logger.info("Created empty instance of table")

        char_index: int = 0
        for col in range(width.raw_value):
            for row in range(height.raw_value):
                table[row, col] = data[char_index]
                logger.info(
                    "Setting table data at indexes: row = %s, col = %s, data = %s",
                    row,
                    col,
                    data[char_index]
                )
                char_index += 1

        logger.info("Finished creating table. Table data:\n %s \n", table)

        return table
