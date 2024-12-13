from typing import Tuple

from combined_languages.theory_of_information.backend.fifth_semestr.fifth_laboratory.scripts.decreasing_matrix.base import \
    decrease_matrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.verification_systematic_matrix import \
    HSystematicMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.registry import Registry


def punch_the_code(h_sys: HSystematicMatrix, indexes_to_delete: Tuple[Tuple[int, int], ...]) -> HSystematicMatrix:
    """
    Перфорация матрицы, здесь пользователь сам определяет на сколько надо уменьшить.
    Удаление происходит по принципу пересечения.
    То есть, если индекс (1, 1), то полностью удаляется строка с индексом 1 и столбец с индексом 1.
    :param h_sys: Проверочная систематическая матрица.
    :param indexes_to_delete: Кортеж из индексов, под которыми мы должны удалить значения.
    """
    result = HSystematicMatrix(decrease_matrix(h_sys, indexes_to_delete))

    Registry.log("Матрица после перфорации матрицы", result.matrix.tolist())

    return result


def main() -> None:
    matrix = [
        [1, 1, 0, 1, 1, 0, 0, 0],
        [1, 0, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 0, 1]
    ]

    indexes_to_delete = ((1, 1),)

    new_matrix = punch_the_code(HSystematicMatrix(matrix), indexes_to_delete)

    print(new_matrix)


if __name__ == '__main__':
    main()
