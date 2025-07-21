from abc import abstractmethod, ABC
from typing import Final

from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.cipher_table.services.id_generator import CipherTableIdGenerator
from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension


class TableCreationStrategy(ABC):
    def __init__(
            self,
            id_generator: CipherTableIdGenerator
    ) -> None:
        self._id_generator: Final[CipherTableIdGenerator] = id_generator

    @abstractmethod
    def create_table(
            self,
            data: str,
            width: TableDimension,
            height: TableDimension
    ) -> Table:
        raise NotImplementedError
