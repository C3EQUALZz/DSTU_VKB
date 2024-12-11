import numpy as np

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.verification_systematic_matrix import \
    HSystematicMatrix


def extend_the_code(h_sys: HSystematicMatrix) -> HSystematicMatrix:
    h_sys = np.vstack((np.ones(h_sys.shape[1], dtype=int), h_sys.matrix)).tolist()
    new_column = []

    for row in h_sys:
        new_column.append(sum(x == 1 for x in row) % 2)

    new_column = np.array(new_column).reshape(-1, 1)

    extended_matrix = np.hstack((new_column, h_sys))

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
