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


def create_table_of_error_vectors_and_syndromes(verification_systematic_matrix_transposed: "HSystematicMatrix"):
    n = len(verification_systematic_matrix_transposed)
    vector = np.vstack((np.zeros(n, dtype=int), np.fliplr(np.diag(np.ones(n, dtype=int)))))
    vector_of_errors: np.ndarray[np.ndarray[int]] = cast(np.ndarray[np.ndarray[int]], vector)
    syndromes = vector_of_errors @ verification_systematic_matrix_transposed
    return TableOfErrorVectorsAndSyndromes(vector_of_errors, syndromes)
