"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""
import os
from pprint import pprint

from sqlalchemy import text
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
    return [country.name for country in SESSION.query(Country).filter(Country.name.like('A%')).all()]


def second_question(k=None) -> str:
    """
    Для БД из задания 1, выведите все улицы, которые встречаются более чем в 5 городах.
    """
    query = text("""
    SELECT main.cities.name
    FROM main.cities, main.streets
    WHERE main.streets.city_id == main.cities.id
    GROUP BY main.streets.city_id
    HAVING COUNT(main.streets.city_id) > 5
    """)
    return '\n'.join(row[0] for row in SESSION.execute(query))


def third_question(k=None):
    """
    Для БД из задания 6 выведите все улицы, для страны РФ
    """
    country_name = 'РФ'  # Замените на фактическое название страны

    # Находим страну по названию
    country = SESSION.query(Country).filter_by(name=country_name).first()

    if country:
        # Если страна найдена, выводим все улицы для неё
        streets = (
            SESSION.query(Street.name)
            .join(City, Street.city_id == City.id)
            .join(Country, City.country_id == Country.id)
            .filter(Country.name == country_name)
            .all()
        )
        return '\n'.join(street.name for street in streets)


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
