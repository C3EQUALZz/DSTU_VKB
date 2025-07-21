from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.cipher_table.services.table_creation.base import TableCreationStrategy
from typing import Final

from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension


class TableCreationContext:
    def __init__(self, strategy: TableCreationStrategy) -> None:
        self._strategy: Final[TableCreationStrategy] = strategy

    def __call__(
            self,
            data: str,
            width: TableDimension,
            height: TableDimension
    ) -> Table:
        return self._strategy.create_table(data=data, width=width, height=height)
