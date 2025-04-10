"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""

import re
from itertools import chain

import numpy as np
from python_language.programming_languages_python.first_laba_lang.tutor import \
    safe_eval


def first_question(n: str):
    """
    Пусть дана матрица чисел размером NxN. Представьте данную матрицу в виде списка.
    Выведите результат сложения всех элементов матрицы.
    Ввести только одну цифру, генерируется случайная квадратная матрица с введенным размером
    """
    matrix = np.random.randint(1000, size=(int(n), int(n)))

    # linear = lambda data: [data] if isinstance(data, np.int64) else sum(map(linear, data), [])
    return "\n".join(
        (
            f"Наша матрица:\n {np.matrix(matrix)}",
            f"Cумма: {matrix.sum()}",
            f"Представление данной матрицы в виде строки: {list(chain.from_iterable(matrix))}",
        )
    )


def second_question(raw_string: str):
    """
    Пусть дан список из десяти элементов.
    Вариант 1. Удалите первые 2 элемента и добавьте 2 новых. Выведите список на экран
    Пример ввода [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] [1, 2]
    """
    old_list, items_to_add = map(safe_eval, re.findall(r"\[.*?\]", raw_string))
    return f"До: {old_list}\nПосле: {old_list[2:] + items_to_add}"


def third_question(k=None) -> str:
    """
    Пусть дан журнал по предмету "Информационные технологии" представлен в виде списка my_len.
    Вариант 1. Выведите список студентов конкретной группы построчно в виде:
    <Название группы>
        <ФИО>
        <ФИО>
    Ничего вводить не надо
    """
    my_len = [
        ["БО-331101", ["Акулова Алена", "Бабушкина Ксения"]],
        ["БОВ-421102", ["Карпов Роман", "Лёза Алексей"]],
        ["БО-331103", ["Крячков Игнат", "Ибрагим Гусейнов"]],
        ["ВПМК-41", ["Егор Гришков", "Анисимов Ярослав"]],
    ]
    res_str = ""
    for group, humans in my_len:
        res_str += (
            f"{group: ^{len(max(humans, key=len))}}\n"
            + "\n".join(f"{human}" for human in humans)
            + "\n\n"
        )
    return res_str


def fourth_question(k=None):
    """
    Пусть журнал по предмету "Информационные технологии" представлен в виде списка my_len.
    Вариант 1. Выведите всех студентов (и их группы), если фамилия студента начинается на букву А.
    Ничего вводить не надо
    """
    my_len = [
        ["БО-331101", ["Акулова Алена", "Бабушкина Ксения"]],
        ["БОВ-421102", ["Карпов Роман", "Лёза Алексей"]],
        ["БО-331103", ["Крячков Игнат", "Гусейнов Ибрагим"]],
        ["ВПМК-41", ["Гришков Егор", "Анисимов Ярослав"]],
    ]
    res_str = ""
    for group, humans in my_len:
        if temporary_storage := [human for human in humans if human.startswith("А")]:
            res_str += (
                f"{group: ^{len(max(temporary_storage, key=len))}}\n"
                + "\n".join(f"{human}" for human in temporary_storage)
                + "\n\n"
            )
    return res_str


def main():
    match input("Введите номер задания "):
        case "1":
            print(first_question(input("Введите размерность матрицы. ")))
        case "2":
            print(
                second_question(
                    input(
                        "Введите список, состоящий из 10 элементов и через пробел второй, как в repr "
                    )
                )
            )
        case "3":
            print(third_question())
        case "4":
            fourth_question()
        case _:
            print("Вы выбрали неверный номер ")


if __name__ == "__main__":
    main()
