"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""
import os
from db_creation import create_database
from pprint import pprint

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_creation.tables import Position, Department, Teacher


def first_question():
    """
    Представить таблицы в виде структур языка Python
    """
    if not os.path.exists("database.db"):
        create_database()

    engine = create_engine('sqlite:///database.db', echo=False)
    session = sessionmaker(bind=engine)()
    # SQL-запрос для извлечения данных из нескольких таблиц
    # Join объединяет наши данные, чтобы они были вместе
    query_result = session.query(Teacher, Position, Department).join(Position).join(Department).all()

    data_dict = {}
    for teacher, position, department in query_result:
        data_dict[teacher.id] = {
            'name': teacher.name,
            'age': teacher.age,
            'position': {'id': position.id, 'title': position.title},
            'department': {'id': department.id, 'title': department.title, 'institute': department.institute}
        }

    return data_dict


def second_question():
    ...


def third_question():
    ...


def fourth_question():
    ...


def main() -> None:
    match input("Выберите номер задания "):
        case "1":
            pprint(first_question())
        case "2":
            pprint(second_question(), sort_dicts=False)
        case "3":
            pprint(third_question())
        case "4":
            pprint(fourth_question())
        case _:
            print("Вы выбрали неверное задание ")


if __name__ == "__main__":
    main()
