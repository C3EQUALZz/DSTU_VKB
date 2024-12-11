from collections.abc import Mapping
from typing import Literal, List, Optional, Tuple, Final

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


def get_info_about_matrix(matrix, type_matrix):
    code_table, _ = get_info_for_encoding(matrix, type_matrix)
    _ = find_errors(code_table)


def execute(
        algorithm: Literal["shortening", "extension", "perforation", "completion"],
        matrix: List[List[int]],
        type_matrix: Literal["G", "H"],
        indexes: Optional[Tuple[Tuple[int, int], ...]] = None,
) -> Mapping[str, Mapping[str, str]]:
    Registry.clear()

    if algorithms[algorithm][1] != type_matrix:
        raise ValueError("Данный алгоритм не работает с этим типом матрицы")

    if type_matrix == "G":
        matrix = GMatrix(matrix=matrix)
    elif type_matrix == "H":
        matrix = HMatrix(matrix=matrix)
    else:
        raise ValueError("Неизвестный тип матрицы")

    get_info_about_matrix(matrix, type_matrix)

    results["До применения алгоритма"] = Registry.get_all_info()

    Registry.clear()

    if algorithm in ("shortening", "perforation"):
        algorithms[algorithm][0](matrix, indexes)
    else:
        algorithms[algorithm][0](matrix)

    results["После применения алгоритма"] = Registry.get_all_info()

    Registry.clear()

    return results


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
