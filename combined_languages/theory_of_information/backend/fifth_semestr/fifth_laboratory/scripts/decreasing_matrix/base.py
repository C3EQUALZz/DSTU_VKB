from typing import List, Tuple

import numpy as np

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import \
    SystematicMatrix


def decrease_matrix(
        sys_matrix: SystematicMatrix,
        indexes_to_delete: Tuple[Tuple[int, int], ...]
) -> List[List[int]]:
    """
    Базовая функция для удаления элементов для алгоритмов: "Перфорация", "Укорочение".
    Написана с точки зрения DRY, чтобы не было дублирования логики.
    """
    rows_to_delete = [x[0] for x in indexes_to_delete]
    columns_to_delete = [x[1] for x in indexes_to_delete]

    new_matrix = np.delete(sys_matrix.matrix, rows_to_delete, axis=0)  # Удаляем строки
    new_matrix = np.delete(new_matrix, columns_to_delete, axis=1)

    return new_matrix.tolist()
