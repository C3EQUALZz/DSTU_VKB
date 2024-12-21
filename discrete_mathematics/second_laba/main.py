"""
Выполнил Ковалев Данил ВКБ22
Лабораторная 2
Для булевой функции от трех переменных вычислите матрицы:
a) перехода от таблицы к многочлену Жегалкина и обратную (получить полином Жегалкина с помощью БПФ)

б) переход от полинома Жегалкина к вектору

"""

from from_vector_to_zhegalkin import Polynom
from from_zhegalkin_to_vector import vector_from_polynom
from typing import NoReturn


def first_question() -> None | NoReturn:
    """
    Ввод данных для пункта а), отсюда все вызывается
    Пример для ввода: 0 1 1 1 0 0 1 1
    """
    input_data: str = input("Введите функцию - вектор для Полинома Жегалкина ")
    # Ввод может быть с пробелом, а может и без, поэтому тут поставлена проверка такая.
    # Если есть хотя бы один пробел, тогда я буду делать split()
    condition: int = any(x.isspace() for x in input_data)
    # Здесь у меня кортеж в зависимости от того, как буду передавать его в класс
    # Если без пробелов, то я просто делю поэлементно tuple("0101") -> ("0", "1", "0", "1"), дальше очевидно все
    data: list[int] = list(map(int, input_data.split())) if condition else [int(x) for x in tuple(input_data)]
    try:
        result = Polynom(data)
        result.print_res()
    except ValueError:
        raise ValueError("Вы использовали не целые числа при записи")


def second_question():
    """
    Ввод данных для пункта б), отсюда все вызывается
    Пример для ввода: z ^ y ^ y*z ^ x*z ^ x*y*z
    """
    print(vector_from_polynom(input("Введите ваш полином: ")))


def main() -> None:
    """
    Точка запуска программы, здесь происходит запуск программы
    """
    match input('Что вы хотите сделать?\n1.Из вектора полином Жегалкина;\n2.Из полинома Жегалкина вектор\n'):
        case "1" | "Из вектора полином Жегалкина" | "1.Из вектора полином Жегалкина":
            first_question()
        case "2" | "Из полинома Жегалкина вектор" | "2.Из полинома Жегалкина вектор":
            second_question()
        case _:
            print("Вы не выбрали нужное задание!")


if __name__ == "__main__":
    main()
