from typing import cast

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.code_table import \
    create_code_table
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.generator_systematic_matrix import \
    GSystematicMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.factories.matrix import \
    MatrixFactory


def create_table_for_encoding(matrix: list[list[int]], type_matrix: str):
    gen_or_check_matrix = MatrixFactory.create(matrix, type_matrix)
    gen_or_check_systematic_matrix = gen_or_check_matrix.to_systematic_form()
    inverse_systematic_matrix = gen_or_check_systematic_matrix.find_another_type_matrix()

    if inverse_systematic_matrix.__class__.__name__ == "GSystematicMatrix":
        matrix_for_table = cast(GSystematicMatrix, inverse_systematic_matrix)
    elif inverse_systematic_matrix.__class__.__name__ == "HSystematicMatrix":
        matrix_for_table = cast(GSystematicMatrix, gen_or_check_systematic_matrix)
    else:
        raise ValueError("Неправильный тип матрицы")

    return create_code_table(matrix_for_table)
