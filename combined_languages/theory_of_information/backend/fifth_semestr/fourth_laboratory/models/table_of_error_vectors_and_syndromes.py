from dataclasses import dataclass, asdict
from typing import TYPE_CHECKING, cast, Iterable
import itertools

import numpy as np

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.registry import Registry

if TYPE_CHECKING:
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.verification_systematic_matrix import \
        HSystematicMatrix
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.code_table import \
        Errors


@dataclass
class TableOfErrorVectorsAndSyndromes:
    errors: np.ndarray[np.ndarray[int]]
    syndromes: np.ndarray[np.ndarray[int]]

    def __post_init__(self) -> None:
        data = asdict(self)

        for key, value in data.items():
            data[key] = value.tolist()

        Registry.log(f"Таблица синдромов и векторов ошибок {self.__class__.__name__}", data)


def create_table_of_error_vectors_and_syndromes(
        verification_systematic_matrix_transposed: "HSystematicMatrix",
        errors: "Errors"
) -> TableOfErrorVectorsAndSyndromes:
    """
    Функция, которая создает таблицу векторов ошибок и синдромов.
    Таблица векторов - это матрица, где первая строка состоит только из 0.
    В последующих строках есть единственная 1, которая с каждой новой строкой сдвигается влево.

    :param verification_systematic_matrix_transposed: Транспонированная проверочная систематическая матрица Hsys^T.
    :return: Возвращает объект, представляющий собой совокупность таблицы векторов и синдромов.
    """
    n = len(verification_systematic_matrix_transposed)
    count_of_ones = errors.count_of_corrections
    count_of_zeros = n - errors.count_of_corrections
    elements = [0] * count_of_zeros + [1] * count_of_ones
    sorted_raws = cast(Iterable, sorted(set(itertools.permutations(elements, n)), key=lambda raw: -raw.index(1)))
    vector = np.vstack((np.zeros(n, dtype=int), sorted_raws))
    vector_of_errors = cast(np.ndarray[np.ndarray[int]], vector)
    syndromes = (vector_of_errors @ verification_systematic_matrix_transposed.matrix) % 2
    return TableOfErrorVectorsAndSyndromes(vector_of_errors, syndromes)
