import numpy as np
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.verification_systematic_matrix import \
        HSystematicMatrix


@dataclass
class TableOfErrorVectorsAndSyndromes:
    errors: np.ndarray[np.ndarray[int]]
    syndromes: np.ndarray[np.ndarray[int]]


def create_table_of_error_vectors_and_syndromes(
        verification_systematic_matrix_transposed: "HSystematicMatrix"
) -> TableOfErrorVectorsAndSyndromes:
    """
    Функция, которая создает таблицу векторов ошибок и синдромов.
    Таблица векторов - это матрица, где первая строка состоит только из 0.
    В последующих строках есть единственная 1, которая с каждой новой строкой сдвигается влево.

    :param verification_systematic_matrix_transposed: Транспонированная проверочная систематическая матрица Hsys^T.
    :return: Возвращает объект, представляющий собой совокупность таблицы векторов и синдромов.
    """
    n = len(verification_systematic_matrix_transposed)
    vector = np.vstack((np.zeros(n, dtype=int), np.fliplr(np.diag(np.ones(n, dtype=int)))))
    vector_of_errors = cast(np.ndarray[np.ndarray[int]], vector)
    syndromes = (vector_of_errors @ verification_systematic_matrix_transposed.matrix) % 2
    return TableOfErrorVectorsAndSyndromes(vector_of_errors, syndromes)
