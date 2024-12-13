import numpy as np

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.generator_systematic_matrix import \
    GSystematicMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.registry import Registry


def refill_code(g_sys: GSystematicMatrix) -> GSystematicMatrix:
    """
    Пополнение кода.
    Данный алгоритм работает с порождающей систематической матрицей.
    Принцип состоит в том, чтобы добавить строку, состоящую из "1" сверху.
    """

    result = GSystematicMatrix(np.vstack((np.ones(len(g_sys[0])), g_sys.matrix)).tolist())

    Registry.log("Матрица после пополнения кода", result.matrix.tolist())

    return result


if __name__ == '__main__':
    matrix = [
        [1, 0, 0, 0, 1, 1, 0, 1],
        [0, 1, 0, 0, 1, 0, 1, 1],
        [0, 0, 1, 0, 1, 0, 0, 1],
        [0, 0, 0, 1, 0, 1, 1, 1]
    ]

    print(refill_code(GSystematicMatrix(matrix)))
