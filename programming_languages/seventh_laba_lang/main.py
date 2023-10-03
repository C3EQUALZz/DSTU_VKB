"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""
from mimesis import Person
from programming_languages.fifth_laba_lang.main import create_csv_file
import csv


def first_question():
    person = Person()
    d = {"age": person.age(),
         "name": person.name(),
         "academic_degree": person.academic_degree(),
         "height": person.height(),
         "gender": person.gender()}
    print(f"Количество ключей у словаря - {len(d.keys())}")


def second_question():
    create_csv_file()
    with open("students.csv", encoding="UTF-8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        