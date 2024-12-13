from collections.abc import Mapping
from copy import copy
from typing import Literal, List, Optional, Tuple, Final

import numpy as np

from combined_languages.theory_of_information.backend.fifth_semestr.fifth_laboratory.scripts.decreasing_matrix.code_shortening import \
    short_the_code
from combined_languages.theory_of_information.backend.fifth_semestr.fifth_laboratory.scripts.decreasing_matrix.perforation import \
    punch_the_code
from combined_languages.theory_of_information.backend.fifth_semestr.fifth_laboratory.scripts.increasing_matrix.code_extenstion import \
    extend_the_code
from combined_languages.theory_of_information.backend.fifth_semestr.fifth_laboratory.scripts.increasing_matrix.refill_code import \
    refill_code
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.code_table import \
    find_errors
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.generator_matrix import \
    GMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.verification_matrix import \
    HMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.factories.systematic import \
    SystematicMatrixFactory
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.helpers import \
    get_info_for_encoding
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.registry import Registry

algorithms: Final = {
    "shortening": (short_the_code, "G"),
    "extension": (extend_the_code, "H"),
    "perforation": (punch_the_code, "H"),
    "completion": (refill_code, "G")
}

results = {}

def replace_numpy_with_list(data):
    if isinstance(data, dict):
        return {key: replace_numpy_with_list(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_numpy_with_list(item) for item in data]
    elif isinstance(data, np.ndarray):
        return data.tolist()  # Преобразуем numpy массив в список
    else:
        return data


def get_info_about_matrix(matrix, type_matrix):
    code_table, _ = get_info_for_encoding(matrix.matrix, type_matrix)
    _ = find_errors(code_table)


def execute(
        algorithm: Literal["shortening", "extension", "perforation", "completion"],
        matrix: List[List[int]],
        type_matrix: Literal["G", "H"],
        indexes: Optional[Tuple[Tuple[int, int], ...]] = None,
):
    Registry.clear()

    if algorithms[algorithm][1] != type_matrix:
        raise ValueError("Данный алгоритм не работает с этим типом матрицы")

    if type_matrix == "G":
        matrix = GMatrix(matrix=matrix)
    elif type_matrix == "H":
        matrix = HMatrix(matrix=matrix)
    else:
        raise ValueError("Неизвестный тип матрицы")

    systematic_matrix = SystematicMatrixFactory.create(matrix, type_matrix)

    get_info_about_matrix(systematic_matrix, type_matrix)

    results["До применения алгоритма"] = copy(Registry.get_all_info())

    Registry.clear()

    if algorithm in ("shortening", "perforation"):
        systematic_matrix = algorithms[algorithm][0](matrix, indexes)
    else:
        systematic_matrix = algorithms[algorithm][0](matrix)

    get_info_about_matrix(systematic_matrix, type_matrix)

    results["После применения алгоритма"] = copy(Registry.get_all_info())

    Registry.clear()

    return replace_numpy_with_list(results)


if __name__ == "__main__":
    m = [
        [1, 0, 0, 0, 1, 1, 0, 1],
        [0, 1, 0, 0, 1, 0, 1, 1],
        [0, 0, 1, 0, 1, 0, 0, 1],
        [0, 0, 0, 1, 0, 1, 1, 1]
    ]
    print(
        execute(
            "shortening",
            matrix=m,
            type_matrix="G",
            indexes=((1, 1),)
        )
    )
