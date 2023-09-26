import os
import csv
from mimesis import Person
from random import randint
from prettytable import PrettyTable


def first_question(path: str = os.getcwd()):
    """
    Пусть дана некоторая директория (папка). Подсчитайте количество файлов в данной директории (папке).
    Выведите на экран
    """
    print(sum(len(files) for root, dirs, files in os.walk(fr"{path}")))


def create_csv_file():
    person = Person()
    with open("students.csv", mode='w', encoding="UTF-8", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(['№', "ФИО", "Возраст", "Группа"])
        writer.writerows(
            [
                [
                    i,
                    person.full_name(),
                    person.age(),
                    f"БО - {''.join(str(randint(0, 9)) for _ in range(6))}"
                ]
                for i in range(100)
            ]
        )


def second_question():
    table = PrettyTable()
    if not os.path.exists("students.csv"):
        create_csv_file()
    with open("students.csv", encoding="UTF-8") as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        table.field_names = reader.__next__()
        table.add_rows(sorted(reader, key=lambda row: row[1].split()[0]))
    print(table)



