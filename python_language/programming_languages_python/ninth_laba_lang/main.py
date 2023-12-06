"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""
from python_language.programming_languages_python.eighth_laba_lang.main import first_question as students_dictionary
from pprint import pprint


def first_question(string: str) -> dict:
    """
    Пусть список студентов представлен в виде структуры {№: [ФИО, Возраст, группа]}.
    Реализуйте функционал по добавлению нового студента (данные вводятся через консоль).
    Пример ввода: 15 Василий Теркин 28 ВМО-42
    """
    string = string.split()
    string[1:3] = [' '.join(string[1:3])]
    return students_dictionary("../eighth_laba_lang/students.csv") | {string[0]: string[1:]}


def second_question(string: str) -> dict:
    """
    Пусть список студентов представлен в виде структуры {№: [ФИО, Возраст, группа]}.
    Реализуйте функционал по изменению всех данных о студенте (поиск по №).
    Пример ввода: 3 Егор Гришков 18 ВПР-22
    """
    data = students_dictionary("../eighth_laba_lang/students.csv")
    string = string.split()
    string[1:3] = [' '.join(string[1:3])]
    data[string[0]] = string[1:]
    return data


def third_question(index: str):
    """
    Пусть список студентов представлен в виде структуры {№: [ФИО, Возраст, группа]}.
    Реализуйте функционал по удалению данных о студенте (поиск по №).
    Пример ввода: 0
    """
    data = students_dictionary("../eighth_laba_lang/students.csv")
    return data.pop(index)


def fourth_question(index: str):
    """
    Пусть список студентов представлен в виде структуры {№: [ФИО, Возраст, группа]}.
    Выведите информацию о студенте с конкретным №.
    Пример ввода: 3
    """
    return students_dictionary("../eighth_laba_lang/students.csv")[index]


def main() -> None:
    match input("Выберите номер задания "):
        case "1":
            pprint(first_question(input("Введите значения у студента, как в примере doc: ")), sort_dicts=False)
        case "2":
            pprint(second_question(input("Введите значение у студента, как в docstring ")), sort_dicts=False)
        case "3":
            pprint(third_question(input("Введите номер студента ")))
        case "4":
            pprint(fourth_question(input("Введите номер студента ")))


if __name__ == "__main__":
    main()
