from typing import Tuple

from combined_languages.theory_of_information.backend.fifth_semestr.fifth_laboratory.scripts.decreasing_matrix.base import \
    decrease_matrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.generator_systematic_matrix import \
    GSystematicMatrix


def short_the_code(g_sys: GSystematicMatrix, indexes_to_delete: Tuple[Tuple[int, int], ...]) -> GSystematicMatrix:
    """
    Укорочение матрицы, здесь пользователь сам определяет на сколько надо уменьшить.
    Удаление происходит по принципу пересечения.
    То есть, если индекс (1, 1), то полностью удаляется строка с индексом 1 и столбец с индексом 1.
    :param g_sys: Порождающая систематическая матрица
    :param indexes_to_delete: кортеж из индексов, под которыми мы должны удалить значения.
    """
    return GSystematicMatrix(decrease_matrix(g_sys, indexes_to_delete))


def main() -> None:
    matrix = [
        [1, 0, 0, 0, 1, 1, 0, 1],
        [0, 1, 0, 0, 1, 0, 1, 1],
        [0, 0, 1, 0, 1, 0, 0, 1],
        [0, 0, 0, 1, 0, 1, 1, 1]
    ]

    indexes_to_delete = ((1, 1),)

    new_matrix = short_the_code(GSystematicMatrix(matrix), indexes_to_delete)

    print(new_matrix)


if __name__ == '__main__':
    main()
