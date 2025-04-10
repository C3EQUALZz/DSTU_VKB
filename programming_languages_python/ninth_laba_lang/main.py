"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""

import csv
########################################################################################################################
import os
from pprint import pprint

########################################################################################################################
from python_language.programming_languages_python.eighth_laba_lang.main import \
    first_question as students_dictionary
from python_language.programming_languages_python.seventh_laba_lang.main import \
    create_csv_file

FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.csv")

if not os.path.exists(FILE_PATH):
    create_csv_file(FILE_PATH)


def first_question(string: str) -> dict:
    """
    Пусть список студентов представлен в виде структуры {№: [ФИО, Возраст, группа]}.
    Реализуйте функционал по добавлению нового студента (данные вводятся через консоль).
    Пример ввода: 15 Василий Теркин 28 ВМО-42
    """
    string = string.split()
    string[1:3] = [" ".join(string[1:3])]
    new_dictionary = students_dictionary(FILE_PATH) | {string[0]: string[1:]}

    with open(FILE_PATH, "w") as f:
        csv_writer = csv.writer(f, delimiter=";")
        csv_writer.writerow(["№", "ФИО", "Возраст", "Группа"])
        csv_writer.writerows([[key, *value] for key, value in new_dictionary.items()])

    return students_dictionary(FILE_PATH)


def second_question(string: str) -> dict:
    """
    Пусть список студентов представлен в виде структуры {№: [ФИО, Возраст, группа]}.
    Реализуйте функционал по изменению всех данных о студенте (поиск по №).
    Пример ввода: 3 Егор Гришков 18 ВПР-22
    """
    string = string.split()

    string[1:3] = [" ".join(string[1:3])]
    new_dictionary = students_dictionary(FILE_PATH) | {string[0]: string[1:]}

    with open(FILE_PATH, "w", encoding="UTF-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")
        csv_writer.writerow(["№", "ФИО", "Возраст", "Группа"])
        csv_writer.writerows([[key, *value] for key, value in new_dictionary.items()])

    return students_dictionary(FILE_PATH)


def third_question(index: str):
    """
    Пусть список студентов представлен в виде структуры {№: [ФИО, Возраст, группа]}.
    Реализуйте функционал по удалению данных о студенте (поиск по №).
    Пример ввода: 0
    """
    data = students_dictionary(FILE_PATH)
    data.pop(index)

    with open(FILE_PATH, "w", encoding="UTF-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")

        csv_writer.writerow(["№", "ФИО", "Возраст", "Группа"])
        csv_writer.writerows([[key, *value] for key, value in data.items()])

    return students_dictionary(FILE_PATH)


def fourth_question(index: str):
    """
    Пусть список студентов представлен в виде структуры {№: [ФИО, Возраст, группа]}.
    Выведите информацию о студенте с конкретным №.
    Пример ввода: 3
    """
    return students_dictionary(FILE_PATH)[index]


def main() -> None:
    match input("Выберите номер задания "):
        case "1":
            pprint(
                first_question(
                    input("Введите значения у студента, как в примере doc: ")
                ),
                sort_dicts=False,
            )
        case "2":
            pprint(
                second_question(input("Введите значение у студента, как в docstring ")),
                sort_dicts=False,
            )
        case "3":
            pprint(third_question(input("Введите номер студента ")), sort_dicts=False)
        case "4":
            pprint(fourth_question(input("Введите номер студента ")))


if __name__ == "__main__":
    main()
