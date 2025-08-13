from dataclasses import dataclass

from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.common.entities.base_entity import BaseEntity
from cryptography_methods.domain.double_square_whitestone.values.table_id import WhiteStoneTableID


@dataclass(eq=False, kw_only=True)
class DoubleTableWhitestone(BaseEntity[WhiteStoneTableID]):
    left_table: Table
    right_table: Table

    def __str__(self) -> str:
        return "Double Table" + "\n" + f"Left table: {self.left_table}" + "\n" + f"Right table: {self.right_table}"
