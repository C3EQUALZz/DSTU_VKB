from typing import cast, TYPE_CHECKING, List, Tuple, Literal

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.code_table import \
    create_code_table
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.generator_systematic_matrix import \
    GSystematicMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.verification_systematic_matrix import \
    HSystematicMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.factories.matrix import \
    MatrixFactory
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.registry import Registry

if TYPE_CHECKING:
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.code_table import \
        CodeTable


def get_info_for_encoding(
        matrix: List[List[int]],
        type_matrix: Literal["G", "H"]
) -> Tuple["CodeTable", GSystematicMatrix]:
    """
    Не совсем корректно делаю, что возвращаю в кортеже подобное. Неправильно построил архитектуру...
    В данной функции в начале создается с помощью фабрики матрица с нужным типом.
    После этого приводим к систематической форме и ищем обратную матрицу.
    Нам нужно в любом случае вернуть GSystematicMatrix, поэтому я на всякий случай инвертирую, а потом проверяю для возврата.
    :param matrix: Матрица, введенная пользователем.
    :param type_matrix: Тип матрицы H или G
    :returns: кортеж, состоящий из таблицы информационных и кодовых слов, а также систематическая матрица.
    """
    gen_or_check_matrix = MatrixFactory.create(matrix, type_matrix)
    gen_or_check_systematic_matrix = gen_or_check_matrix.to_systematic_form()
    inverse_systematic_matrix = gen_or_check_systematic_matrix.find_another_type_matrix()

    if inverse_systematic_matrix.__class__.__name__ == "GSystematicMatrix":
        matrix_for_table = cast(GSystematicMatrix, inverse_systematic_matrix)
    elif inverse_systematic_matrix.__class__.__name__ == "HSystematicMatrix":
        matrix_for_table = cast(GSystematicMatrix, gen_or_check_systematic_matrix)
    else:
        raise ValueError(f"Неправильный тип матрицы {inverse_systematic_matrix.__class__.__name__}")

    return create_code_table(matrix_for_table), matrix_for_table


def get_verification_systematic_transposed_matrix(
        matrix: List[List[int]],
        type_matrix: Literal["G", "H"]
) -> "HSystematicMatrix":
    """
    Получение Hsys^T матрицы из матрицы, введенной пользователем.
    Здесь в начале с помощью фабрики создается G или H матрица.
    После этого приводится в систематическую форму.
    :param matrix: Матрица, введенная пользователем.
    :param type_matrix: Порождающая (G) или проверочная (H) матрица.
    :returns: Проверочная систематическая матрица, которая была транспонирована (Hsys^T)
    """
    gen_or_check_matrix = MatrixFactory.create(matrix, type_matrix)
    gen_or_check_systematic_matrix = gen_or_check_matrix.to_systematic_form()
    inverse_systematic_matrix = gen_or_check_systematic_matrix.find_another_type_matrix()

    if inverse_systematic_matrix.__class__.__name__ == "HSystematicMatrix":
        result = cast(HSystematicMatrix, inverse_systematic_matrix.transpose())
    elif inverse_systematic_matrix.__class__.__name__ == "GSystematicMatrix":
        result = cast(HSystematicMatrix, gen_or_check_systematic_matrix.transpose())
    else:
        raise ValueError(f"Неправильный тип матрицы {inverse_systematic_matrix.__class__.__name__}")

    Registry.log("Транспонированная проверочная систематическая матрица HSystematicMatrix", result)

    return result
