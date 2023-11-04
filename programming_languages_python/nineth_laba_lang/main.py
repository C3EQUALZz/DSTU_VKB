"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""
from programming_languages_python.eigth_laba_lang.main import first_question as students_dictionary
from pprint import pprint


def first_question(string: str) -> dict:
    """
    Пусть список студентов представлен в виде структуры {№: [ФИО, Возраст, группа]}.
    Реализуйте функционал по добавлению нового студента (данные вводятся через консоль).
    Пример ввода: 15 Василий Теркин 28 ВМО-42
    """
    string = string.split()
    string[1:3] = [' '.join(string[1:3])]
    return students_dictionary("../eigth_laba_lang/students.csv") | {string[0]: string[1:]}


def second_question(string: str) -> dict:
    """
    Пусть
    """
    string = string.split()
    string[1:3] = [' '.join(string[1:3])]


def third_question():
    ...


def fourth_question():
    ...


def main() -> None:
    match input("Выберите номер задания "):
        case "1":
            pprint(first_question(input("Введите значения у студента, как в примере doc: ")))
        case "2":
            pprint(second_question())
        case "3":
            pprint(third_question())
        case "4":
            pprint(first_question())


if __name__ == "__main__":
    main()
