"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""

import csv
import os
from pprint import pprint

from mimesis import Person
from python_language.programming_languages_python.fifth_laba_lang.main import \
    create_csv_file

FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.csv")


def first_question(k=None) -> int:
    """
    Пусть дан словарь. Посчитайте и выведите сколько в словаре ключей
    Ничего вводить не надо
    """
    person = Person()
    d = {
        "age": person.age(),
        "name": person.name(),
        "academic_degree": person.academic_degree(),
        "height": person.height(),
        "gender": person.gender(),
    }
    return len(d)


def second_question(k=None) -> dict:
    """
    Пусть дан файл, в котором содержится информация о студентах в виде:
    1;Иванов Иван Иванович;23;БО-111111
    2;Сидоров Семен Семенович;23;БО-111111
    Считайте информацию из файла в структуру: {№: [ФИО, Возраст, Группа], №: [....], №: [....]}
    Ничего вводить не надо
    """
    if not os.path.exists(FILE_PATH):
        create_csv_file(FILE_PATH)
    with open(FILE_PATH, encoding="UTF-8") as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        reader.__next__()
        return {x[0]: x[1:] for x in sorted(reader, key=lambda row: row[1].split()[1])}


def third_question(k=None) -> dict:
    """
    Добавьте к задаче №2 возможность увеличить возраст всех студентов на 1
    Ничего вводить не надо
    """
    data = second_question()
    for key, value in data.items():
        value[1] = int(value[1]) + 1
    return data


def fourth_question(k=None) -> str:
    """
    Добавьте к пользовательскому интерфейсу из задачи №3 возможность сохранения новых данных в файл.
    Ничего вводить не надо
    """
    with open(FILE_PATH[:-4] + "_new.csv", mode="w", encoding="UTF-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(["№", "ФИО", "Возраст", "Группа"])
        data = third_question(1)
        writer.writerows([[k, *data[k]] for k in data])
        return "Выполнено!"


def main():
    match input("Введите номер задания "):
        case "1":
            print(f"Количество ключей у словаря - {first_question()}")
        case "2":
            pprint(second_question(), sort_dicts=False)
        case "3":
            pprint(third_question(), sort_dicts=False)
        case "4":
            fourth_question()
        case _:
            print("Вы выбрали неверный номер ")


if __name__ == "__main__":
    main()
