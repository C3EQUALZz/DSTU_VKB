from typing import List

from app.domain.entities.block_codes.base import SystematicMatrix
from app.domain.entities.block_codes.factories.inverse_matrix import InverseMatrixFactory


class GSystematicMatrix(SystematicMatrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)
        InverseMatrixFactory.register("G", "verification_matrix.HSystematicMatrix")

    def find_another_type_matrix(self) -> "SystematicMatrix":
        return InverseMatrixFactory.create(self, "G")
