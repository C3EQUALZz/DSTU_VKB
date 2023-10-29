from pprint import pprint

import re
import csv


def read_file() -> list:
    with open("students.csv") as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        reader.__next__()
        return list(reader)


def first_question(k=None) -> dict:
    """
    Пусть список студентов представлен в виде структуры [[№, ФИО, Возраст, Группа]...].
    Преобразовать список в словарь вида: {№:[ФИО, Возраст, Группа], ....}
    """
    return {person[0]: person[1:] for person in read_file()}


def second_question(s: str):
    if re.fullmatch(r"[иИ]зменить возраст \w+ на \d+", s):
        for key, value in first_question():
            if value[0]:
                ...


def main() -> None:
    match input("Выберите номер задания "):
        case "1":
            pprint(first_question())
        case "2":
            print("Все студенты, у которых можно увеличить возраст представлены ниже ")
            pprint(first_question())
            pprint(second_question(input("Введите что вы хотите сделать, как сказано в условии ")))


if __name__ == "__main__":
    main()
