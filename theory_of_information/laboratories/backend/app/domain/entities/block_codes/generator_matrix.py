import logging
from typing import List, cast, TYPE_CHECKING

from app.domain.entities.block_codes.base import Matrix
from app.domain.entities.block_codes.factories.systematic import SystematicMatrixFactory

if TYPE_CHECKING:
    from app.domain.entities.block_codes.generator_systematic_matrix import GSystematicMatrix

logger = logging.getLogger(__name__)


class GMatrix(Matrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)
        logger.info(f"{self.__class__.__name__} %s", matrix)
        SystematicMatrixFactory.register("G", "generator_systematic_matrix.GSystematicMatrix")

    def to_systematic_form(self) -> "GSystematicMatrix":
        """
        Находит систематический вид матрицы, удаляя столбцы с единственным значением 1.
        :returns: Модифицированная порождающая матрица в систематическом виде.
        """
        return cast("GSystematicMatrix", SystematicMatrixFactory.create(self, "G"))
