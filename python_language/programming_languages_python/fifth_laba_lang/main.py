"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""
import csv
import os
from random import randint

from mimesis import Person
from prettytable import PrettyTable

FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.csv")


def first_question(path: str):
    """
    Пусть дана некоторая директория (папка). Подсчитайте количество файлов в данной директории (папке).
    Выведите на экран.
    По умолчанию стоит текущая директория (нажмите пробел).
    Вводить надо абсолютный путь для поиска файлов в директории.
    """
    if path.isspace():
        path = os.getcwd()
    return sum(len(files) for root, dirs, files in os.walk(fr"{path}"))


def create_csv_file():
    person = Person()
    with open(FILE_PATH, mode='w', encoding="UTF-8", newline='') as csv_file:
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


def second_question(k=None):
    """
    Пусть дан файл students.csv, в котором содержится информация о студентах в виде:
    №;ФИО;Возраст;Группа
    Вариант 1. Выведите информацию о студентах, отсортировав их по фамилии.
    """
    table = PrettyTable()
    if not os.path.exists(FILE_PATH):
        create_csv_file()
    with open(FILE_PATH, encoding="UTF-8") as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        table.field_names = reader.__next__()
        result = sorted(reader, key=lambda row: row[1].split()[1])
        table.add_rows(result)
    return table, result


def third_question(k=None):
    """
    Добавьте к задаче 2 интерфейс.
    Вариант 1. По увеличению возраста всех студентов на 1.
    """
    table = PrettyTable()
    table.field_names = second_question()[0].field_names
    result = [(row[0], row[1], int(row[2]) + 1, row[3]) for row in second_question()[1]]
    table.add_rows(result)
    return table, result


def fourth_question(k=None):
    """
    Добавьте к пользовательскому интерфейсу из задачи возможность сохранения новых данных обратно в файл
    """
    with open(FILE_PATH[:-4] + "_new.csv", mode="w", encoding="UTF-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(third_question()[0].field_names)
        writer.writerows(third_question()[1])
        return "Выполнено!"


def main():
    match input("Введите номер задания "):
        case "1":
            print(
                first_question(input("Введите путь до файла. По умолчанию стоит текущая директория (нажмите пробел) ")))
        case "2":
            print(second_question()[0])
        case "3":
            print(third_question()[0])
        case "4":
            print(fourth_question())
        case _:
            print("Вы выбрали неверный номер ")


if __name__ == "__main__":
    main()
