"""
Лабораторная работа «Реализация алгоритма кодирования Хаффмана»
Входные данные: какой-то текст или набор символов (и русские буквы и латиница, а также все знаки препинания и пробелы)
Выходные данные: таблица соответствия символа и кодового слова, закодированное предложение,
Задача: реализовать алгоритм кодирования Хаффмана, (т.к. он работает с вероятностями или частотой появления символа
 – необходимо их высчитывать)

Полезные материалы:
- https://youtu.be/y_2toG5-j_M?si=glYeEtgQRedmE7dX
- https://youtu.be/nvCJ7dKC9CE?si=MruEOzHiqpLmZCZ9

"""
import time
import huffman
import logging
import prettytable
import python_language.theory_of_information.core as core_namespace

logger = logging.getLogger(__name__)


def main() -> None:
    while True:
        string_input = input("Введите предложение для кодирование с помощью алгоритма Хаффмана: ")
        dictionary_with_encoded_symbols = huffman.Huffman.encode(string_input)
        encoded = "".join(dictionary_with_encoded_symbols[char] for char in string_input)
        logger.info(f"Длина словаря - {len(dictionary_with_encoded_symbols)}, Закодированное сообщение - {encoded}")

        pretty_table = prettytable.PrettyTable()
        for c in dictionary_with_encoded_symbols:
            pretty_table.add_column(c, [])
        pretty_table.add_row(['\n'.join(dictionary_with_encoded_symbols[c]) for c in dictionary_with_encoded_symbols])

        logger.info("\n" + str(pretty_table))
        time.sleep(0.5)


if __name__ == "__main__":
    core_namespace.setup_logger()
    main()
