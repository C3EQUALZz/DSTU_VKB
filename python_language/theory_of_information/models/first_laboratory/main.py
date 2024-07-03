"""
Лабораторная работа «Реализация алгоритма кодирования Хаффмана»
Входные данные: какой-то текст или набор символов (и русские буквы и латиница, а также все знаки препинания и пробелы)
Выходные данные: таблица соответствия символа и кодового слова, закодированное предложение,
Задача: реализовать алгоритм кодирования Хаффмана, (т.к. он работает с вероятностями или частотой появления символа
 – необходимо их высчитывать)

Требования к языку - Python.

"""
import huffman
import logging
import python_language.theory_of_information.core as core_namespace

logger = logging.getLogger(__name__)


def main() -> None:
    string_input = input("Введите предложение для алгоритма Хаффмана: ")
    dictionary_with_encoded_symbols = huffman.Huffman.encode(string_input)
    encoded = "".join(dictionary_with_encoded_symbols[char] for char in string_input)
    logger.info(f"Длина словаря - {len(dictionary_with_encoded_symbols)}, Длина закодированного сообщения - {encoded}")

    for char in sorted(dictionary_with_encoded_symbols):
        logger.info(f"{char}: {dictionary_with_encoded_symbols[char]}")

    logger.info(f"Результат кодирования: {encoded}")


if __name__ == "__main__":
    core_namespace.setup_logger()
    main()
