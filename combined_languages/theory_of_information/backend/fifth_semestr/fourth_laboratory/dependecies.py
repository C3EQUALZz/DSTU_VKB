from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.helpers import \
    create_table_for_encoding, get_verification_systematic_transposed_matrix
import numpy as np


def generate_errors(word: str, n: int) -> str:
    array = np.array([int(x) for x in word])
    array[::n] = np.logical_not(array[::n])
    return "".join(map(str, array))


def encode(word: str, matrix: list[list[int]], type_matrix: str) -> str:
    code_table = create_table_for_encoding(matrix, type_matrix)
    binary_word = ''.join(format(x, 'b') for x in bytearray(word, 'utf-8'))
    blocks = [list(map(int, binary_word[i:i + len(matrix)])) for i in range(0, len(binary_word), len(matrix))]

    encoded_word = []
    for block in blocks:
        # Находим индекс блока в столбце информационных слов
        index = np.where((code_table.information_words_column == block).all(axis=1))[0][0]
        # Получаем соответствующее значение из столбца кодовых слов
        encoded_block = code_table.code_words_column[index]
        encoded_word.extend(encoded_block)

    return "".join(map(str, encoded_word))


def decode(encoded_with_errors: str, matrix: list[list[int]], type_matrix: str) -> str:
    verification_systematic_matrix_transposed = get_verification_systematic_transposed_matrix(matrix, type_matrix)


def execute(word: str, matrix: list[list[int]], type_matrix: str) -> str:
    encoded_word = encode(word, matrix, type_matrix)
    encoded_word_with_errors = generate_errors(encoded_word, len(matrix[0]))

    return ""


if __name__ == '__main__':
    matrix = [
        [1, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 0, 0, 1],
        [0, 1, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 1]
    ]

    execute(
        "Привет",
        matrix,
        'G'
    )
