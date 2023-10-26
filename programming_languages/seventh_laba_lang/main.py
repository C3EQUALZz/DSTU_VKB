"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""
from mimesis import Person
from programming_languages.fifth_laba_lang.main import create_csv_file
import csv
from pprint import pprint
import os


def first_question(k=None) -> int:
    person = Person()
    d = {"age": person.age(),
         "name": person.name(),
         "academic_degree": person.academic_degree(),
         "height": person.height(),
         "gender": person.gender()}
    return len(d)


def second_question(k=None) -> dict:
    if not os.path.exists("students.csv"):
        create_csv_file()
    with open("students.csv", encoding="UTF-8") as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        reader.__next__()
        return {x[0]: x[1:] for x in sorted(reader, key=lambda row: row[1].split()[1])}


def third_question(k: int):
    data = second_question()
    for key, value in data.items():
        value[1] = int(value[1]) + int(k)
    return data


def fourth_question(k=None):
    with open("students_new.csv", mode="w", encoding="UTF-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(["№", "ФИО", "Возраст", "Группа"])
        data = third_question()
        writer.writerows([[k, *data[k]] for k in data])


def main():
    match input("Введите номер задания "):
        case "1":
            print(f"Количество ключей у словаря - {first_question()}")
        case "2":
            pprint(second_question(), sort_dicts=False)
        case "3":
            pprint(third_question(1), sort_dicts=False)
        case "4":
            fourth_question()
        case _:
            print("Вы выбрали неверный номер ")


if __name__ == "__main__":
    main()
