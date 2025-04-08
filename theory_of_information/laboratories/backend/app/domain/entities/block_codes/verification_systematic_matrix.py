from typing import List

from app.domain.entities.block_codes.base import SystematicMatrix
from app.domain.entities.block_codes.factories.inverse_matrix import InverseMatrixFactory


class HSystematicMatrix(SystematicMatrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)
        InverseMatrixFactory.register("H", "generator_systematic_matrix.GSystematicMatrix")

    def find_another_type_matrix(self) -> "SystematicMatrix":
        return InverseMatrixFactory.create(self, "H")
