import logging
from typing import List, cast

from app.domain.entities.block_codes.base import Matrix
from app.domain.entities.block_codes.factories.systematic import \
    SystematicMatrixFactory
from app.domain.entities.block_codes.verification_systematic_matrix import \
    HSystematicMatrix

logger = logging.getLogger(__name__)


class HMatrix(Matrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)
        logger.info("%s %s", self.__class__.__name__, matrix)
        SystematicMatrixFactory.register(
            "H", "verification_systematic_matrix.HSystematicMatrix"
        )

    def to_systematic_form(self) -> "HSystematicMatrix":
        """
        Находит систематический вид матрицы, удаляя столбцы с единственным значением 1.
        :returns: Модифицированная проверочная матрица в систематическом виде.
        """
        return cast(HSystematicMatrix, SystematicMatrixFactory.create(self, "H"))
