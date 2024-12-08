"""
Задание 3. С клавиатуры ввести значение, индекс которого необходимо найти, если такое значение будет найдено в массиве,
в обратном случае вывести сообщение «элемент в массиве не найден».
Для поиска элемента использовать алгоритм «бинарного поиска»
"""
import sys

from algorithms_and_data_structures.second_laboratory.third_question.binary import binary_search


def main() -> None:
    while True:
        data = input("Введите значения списка через пробел: ").split()

        if not all(x.isdigit() or x[1:].isdigit() for x in data):
            print("Вы ввели не цифры", file=sys.stderr)
            continue

        sorted_data = sorted(map(int, data))

        print(f"Отсортированные элементы по возрастанию: {sorted_data}")

        element = int(input("Введите значение для поиска: "))

        index_of_element = binary_search(sorted_data, element)

        if index_of_element == -1:
            print("Элемент не был найден", file=sys.stderr)
            continue

        print(f"Элемент: {element}, индекс: {index_of_element}")


if __name__ == '__main__':
    main()
