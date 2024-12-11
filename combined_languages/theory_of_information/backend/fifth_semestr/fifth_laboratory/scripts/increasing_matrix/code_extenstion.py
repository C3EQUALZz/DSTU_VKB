import numpy as np

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.verification_systematic_matrix import \
    HSystematicMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.registry import Registry


def extend_the_code(h_sys: HSystematicMatrix) -> HSystematicMatrix:
    """
    Расширение кода.
    Здесь в начале сверху приписываются 1, а потом слева добавляются элементы по правилу:
    Если количество 1 в стоке четное, то "0", в ином случае "1".
    :param h_sys: Систематическая проверочная матрица
    :returns: модифицированная проверочная систематическая матрица.
    """
    h_sys = np.vstack((np.ones(h_sys.shape[1], dtype=int), h_sys.matrix)).tolist()
    new_column = []

    for row in h_sys:
        new_column.append(sum(x == 1 for x in row) % 2)

    new_column = np.array(new_column).reshape(-1, 1)

    extended_matrix = np.hstack((new_column, h_sys))

    result = HSystematicMatrix(extended_matrix.tolist())

    Registry.log("Матрица после расширения кода", result.matrix)

    return HSystematicMatrix(extended_matrix.tolist())


if __name__ == '__main__':
    h = [
        [1, 1, 0, 1, 1, 0, 0, 0],
        [1, 0, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 0, 1]
    ]

    matrix = HSystematicMatrix(h)

    print(extend_the_code(matrix))
