"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""
import os
from pprint import pprint

from sqlalchemy import func
########################################################################################################################
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

########################################################################################################################
from python_language.programming_languages_python.twelfth_laba_lang.db_creation import create_database
from python_language.programming_languages_python.twelfth_laba_lang.db_creation.tables import *

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

if not os.path.exists(file_path):
    create_database()

SESSION = sessionmaker(bind=create_engine(f'sqlite:///{file_path}', echo=False))()


def first_question(k=None) -> list:
    """
    Пусть дана база данных. Используйте нужные структуры данных для её хранения.
    Заполните БД. Выведите все страны, чье название начинается на букву А.
    """
    return [country.title for country in SESSION.query(Country).filter(Country.title.like('A%')).all()]


def second_question(k=None) -> list:
    """
    Для БД из задания 1, выведите все улицы, которые встречаются более чем в 5 городах.
    FIXME
    """
    result = (
        SESSION.query(
            Street.name,
            func.count(City.id).label('city_count')
        )
        .join(City)
        .join(Country)
        .group_by(Street.name)
        .having(func.count(City.id) > 5)
        .all()
    )

    return [street_name for street_name in result]


def third_question(k=None):
    """
    Для БД из задания 6 выведите все улицы, для страны РФ
    """
    ...


def main() -> None:
    match input("Выберите номер задания: "):
        case "1":
            pprint(first_question())
        case "2":
            print(second_question())
        case "3":
            print(third_question())
        case _:
            print("Вы выбрали неверное задание ")


if __name__ == "__main__":
    main()
