from typing import List, cast

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import Matrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.generator_systematic_matrix import \
    GSystematicMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.factories.systematic import \
    SystematicMatrixFactory
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.registry import Registry


class GMatrix(Matrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)
        Registry.log(f"{self.__class__.__name__}", matrix)
        SystematicMatrixFactory.register("G", "generator_systematic_matrix.GSystematicMatrix")

    def to_systematic_form(self) -> "GSystematicMatrix":
        """
        Находит систематический вид матрицы, удаляя столбцы с единственным значением 1.
        :returns: Модифицированная порождающая матрица в систематическом виде.
        """
        return cast(GSystematicMatrix, SystematicMatrixFactory.create(self, "G"))
