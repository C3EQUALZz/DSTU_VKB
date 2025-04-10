"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""

########################################################################################################################
import csv
import os
import re
from pprint import pprint

########################################################################################################################
import python_language.programming_languages_python.eighth_laba_lang.second_subtasks as second_subtasks
import python_language.programming_languages_python.eighth_laba_lang.third_subtasks as third_subtasks
from python_language.programming_languages_python.seventh_laba_lang.main import \
    create_csv_file

FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.csv")


def read_file(path: str = None) -> list:
    if not os.path.exists(path):
        create_csv_file(path)

    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        reader.__next__()
        return list(reader)


def first_question(path: str) -> dict:
    """
    Пусть список студентов представлен в виде структуры [[№, ФИО, Возраст, Группа]...].
    Преобразовать список в словарь вида: {№:[ФИО, Возраст, Группа], ....}
    Ничего вводить не надо
    """
    if path.isspace() or path == "":
        path = FILE_PATH
    return {person[0]: person[1:] for person in read_file(path)}


def second_question(string=None):
    """
    Добавить к задаче №1 для словаря возможность (без преобразования словаря обратно в список).
    1. Увеличить возраст конкретного студента на 1;
    2. Изменить ФИО студента;
    3 Увеличить возраст студента по номеру;
    4. Изменить группу студента. Поиск по ФИО;
    5. Удалить запись о студенте. Поиск по №;
    6. Если возраст студента больше 22 уменьшить его на 1;
    7. Если возраст студента равен 23, удалить его из списка;
    8. У всех студентов с фамилией Иванов увеличить возраст на 1;
    9. У студентов с фамилией Иванов изменить фамилию на Сидоров;
    10. Поменять ФИО и Группа местами;
    """
    patterns_and_functions = {
        r"[иИ]зменить возраст \w+\s\w+ на \d+": second_subtasks.increase_age_by_name,
        r"[иИ]зменить ФИО студента с \w+\s\w+ на \w+\s\w+": second_subtasks.change_name,
        r"[уУ]величить возраст студента под номером №\d+ на \d+": second_subtasks.increase_age_by_number,
        r"[Ии]зменить группу студента \b[A-Za-z]+\s[A-Za-z]+\b на [a-zA-Zа-яА-ЯёЁ]+ - \d+": second_subtasks.change_group_by_name,
        r"[Уу]далить запись о студенте под номером №\d+": second_subtasks.delete_student_by_number,
        r"Если возраст студента больше 22 уменьшить его на 1": second_subtasks.decrease_age_if_more_than_22,
        r"Если возраст студента равен 23, удалить его из списка": second_subtasks.delete_student_if_age_eq_23,
        r"У всех студентов с фамилией Иванов увеличить возраст на 1": second_subtasks.increase_if_surname_ivanov,
        r"У студентов с фамилией Иванов изменить фамилию на Сидоров": second_subtasks.change_ivanov_sidorov,
        r"Поменять ФИО и Группа местами": second_subtasks.swap_places,
    }

    for pattern, function in patterns_and_functions.items():
        if re.fullmatch(pattern, string):
            return function(first_question(), string)
    return "Неправильно ввели"


def third_question(s: str):
    """
    Добавьте к пользовательскому интерфейсу из задачи 2 возможность вывода из словаря:
    1. Списка студентов группы БО - 111111
    2. Списка студентов с номерами от 1 до 10
    3. Списка студентов в возрасте 22 лет
    4. Списка студентов с фамилией 'Иванов'
    5. Списка студентов, чьи фамилии заканчиваются на 'a'
    6. Списка студентов, чей возраст - четное число
    7. Список студентов, если в возрасте студента встречается число 5
    8. Список студентов, если их номера группы длиннее 7 символов
    9. Список студентов (а также информацию о них), если их № - четное число
    10. Список студентов, если их номер группы заканчивается на '1'
    """
    data = first_question()
    return {
        "Вывести список студентов группы БО - 111111": third_subtasks.print_by_group(
            data
        ),
        "Вывести список студентов с номерами от 1 до 10": third_subtasks.print_by_numbers(
            data
        ),
        "Списка студентов в возрасте 22 лет": third_subtasks.print_by_age(data),
        "Список студентов с фамилией Иванов": third_subtasks.print_by_surname(data),
        "Списка студентов, чьи фамилии заканчиваются на 'a'": third_subtasks.print_by_surname_end_a(
            data
        ),
        "Список студентов, чей возраст - это четное число": third_subtasks.print_by_age_even(
            data
        ),
        "Список студентов, если в возрасте студента встречается число 5": third_subtasks.print_by_age_if_5(
            data
        ),
        "Список студентов, если их номера группы длиннее 7 символов": third_subtasks.print_by_length_group(
            data
        ),
        "Список студентов (а также информацию о них), если их № - четное число": third_subtasks.print_by_even_number(
            data
        ),
        "Список студентов, если их номер группы заканчивается на '1'": third_subtasks.print_by_group_ends_1(
            data
        ),
    }[s.strip()]


def main() -> None:
    match input("Выберите номер задания "):
        case "1":
            pprint(first_question("students.csv"))
        case "2":
            pprint(second_question(input("Введите ваше пожелание: ")), sort_dicts=False)
        case "3":
            pprint(third_question(input("Введите условие подпункта: ")))


if __name__ == "__main__":
    main()
