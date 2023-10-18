"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""
from itertools import chain

import numpy as np


def first_question(n: int):
    """
    Пусть дана матрица чисел размером NxN. Представьте данную матрицу в виде списка.
    Выведите результат сложения всех элементов матрицы.
    """
    matrix = np.random.randint(1000, size=(n, n))

    # linear = lambda data: [data] if isinstance(data, np.int64) else sum(map(linear, data), [])
    return '\n'.join((f"Наша матрица:\n {np.matrix(matrix)}", f"Cумма: {matrix.sum()}",
                      f"Представление данной матрицы в виде строки: {list(chain.from_iterable(matrix))}"))


def second_question(lst: list, for_add: str = None):
    """
    Пусть дан список из десяти элементов.
    Вариант 1. Удалите первые 2 элемента и добавьте 2 новых. Выведите список на экран
    """
    if isinstance(lst, str) or for_add is None:
        for_add = lst[lst.find("]") + 1:]
        lst = eval(lst[:lst.find("]") + 1])
    return f"До: {lst}\n" + f"После: {lst[2:] + for_add.split()}"


def third_question(k=None) -> str:
    """
    Пусть дан журнал по предмету "Информационные технологии" представлен в виде списка my_len.
    Вариант 1. Выведите список студентов конкретной группы построчно в виде:
    <Название группы>
        <ФИО>
        <ФИО>
    """
    my_len = [
        ["БО-331101", ["Акулова Алена", "Бабушкина Ксения"]],
        ["БОВ-421102", ["Карпов Роман", "Лёза Алексей"]],
        ["БО-331103", ["Крячков Игнат", "Ибрагим Гусейнов"]],
        ["ВПМК-41", ["Егор Гришков", "Анисимов Ярослав"]]
    ]
    res_str = ''
    for group, humans in my_len:
        res_str += f"{group: ^{len(max(humans, key=len))}}\n" + '\n'.join(f"{human}" for human in humans) + "\n\n"
    return res_str


def fourth_question(k=None):
    """
    Пусть журнал по предмету "Информационные технологии" представлен в виде списка my_len.
    Вариант 1. Выведите всех студентов (и их группы), если фамилия студента начинается на букву А.
    """
    my_len = [
        ["БО-331101", ["Акулова Алена", "Бабушкина Ксения"]],
        ["БОВ-421102", ["Карпов Роман", "Лёза Алексей"]],
        ["БО-331103", ["Крячков Игнат", "Ибрагим Гусейнов"]],
        ["ВПМК-41", ["Егор Гришков", "Анисимов Ярослав"]]
    ]
    res_str = ''
    for group, humans in my_len:
        if temporary_storage := [surname for surname in humans if surname.startswith("А")]:
            print(group, *(f"\t{human}" for human in temporary_storage), sep='\n', end='\n\n')
            res_str += f"{group: ^{len(max(temporary_storage, key=len))}}\n" + '\n'.join(
                f"{human}" for human in temporary_storage) + "\n\n"
    return res_str


def main():
    match input("Введите номер задания "):
        case "1":
            print(first_question(int(input("Введите размерность матрицы. "))))
        case "2":
            print(second_question(eval(input("Введите список, состоящий из 10 элементов, как в repr ")),
                                  input("Введите два элемента через пробел для добавления ")))
        case "3":
            print(third_question())
        case "4":
            fourth_question()
        case _:
            print("Вы выбрали неверный номер ")


if __name__ == "__main__":
    main()
