from typing import List

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import \
    SystematicMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.factories.inverse_matrix import \
    InverseMatrixFactory


class HSystematicMatrix(SystematicMatrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)
        InverseMatrixFactory.register("H", "generator_matrix.GSystematicMatrix")

    def find_another_type_matrix(self) -> "SystematicMatrix":
        return InverseMatrixFactory.create(self, "H")
