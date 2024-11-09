from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.table_of_error_vectors_and_syndromes import \
    create_table_of_error_vectors_and_syndromes
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.helpers import \
    create_table_for_encoding, get_verification_systematic_transposed_matrix
import numpy as np


def generate_errors(word: str, n: int) -> str:
    array = np.array([int(x) for x in word])
    array[::n] = np.logical_not(array[::n])
    return "".join(map(str, array))


def encode(word: str, matrix: list[list[int]], type_matrix: str) -> str:
    code_table = create_table_for_encoding(matrix, type_matrix)
    binary_word = ''.join(format(x, '08b') for x in bytearray(word, 'utf-8'))
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
    code_table = create_table_for_encoding(matrix, type_matrix)
    verification_systematic_matrix_transposed = get_verification_systematic_transposed_matrix(matrix, type_matrix)
    table = create_table_of_error_vectors_and_syndromes(verification_systematic_matrix_transposed)
    count_columns = len(matrix[0])
    blocks = [list(map(int, encoded_with_errors[i:i + count_columns]))
              for i in range(0, len(encoded_with_errors), count_columns)]

    decoded_binary_word = []

    for block in blocks:
        syndrome = np.dot(block, verification_systematic_matrix_transposed.matrix) % 2
        index = np.where((table.syndromes == syndrome).all(axis=1))[0][0]
        errors_block = table.errors[index]
        code_word = (errors_block + block) % 2

        index_of_code_word = np.where((code_table.code_words_column == code_word).all(axis=1))[0][0]
        decoded_block = code_table.information_words_column[index_of_code_word]
        decoded_binary_word.extend(decoded_block)

    binary_word = "".join(map(str, decoded_binary_word))

    byte_chunks = [binary_word[i:i + 8] for i in range(0, len(binary_word), 8)]

    byte_array = bytearray(int(byte, 2) for byte in byte_chunks)

    return byte_array.decode('utf-8')


def execute(word: str, matrix: list[list[int]], type_matrix: str) -> str:
    encoded_word = encode(word, matrix, type_matrix)
    encoded_word_with_errors = generate_errors(encoded_word, len(matrix[0]))
    decoded_word = decode(encoded_word_with_errors, matrix, type_matrix)
    print(decoded_word)

    return ""


if __name__ == '__main__':
    matrix = [
        [1, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 0, 0, 1],
        [0, 1, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 1]
    ]

    execute(
        "Огромное сообщение",
        matrix,
        'G'
    )
