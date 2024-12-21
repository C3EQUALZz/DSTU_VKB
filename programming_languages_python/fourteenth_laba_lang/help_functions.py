"""
В данном модуле описаны вспомогательные функции для вывода таблиц на печать
"""
__all__ = ["generate_table", "generate_train", "generate_student",
           "generate_subscriber", "generate_buyer", "generate_book",
           "generate_animal", "read_from_file", "write_to_file"]

import json
import random

########################################################################################################################
import numpy as np
import requests
from environs import Env
from mimesis import Address, Locale, Datetime
from mimesis.builtins import RussiaSpecProvider
from prettytable import PrettyTable
from russian_names import RussianNames

########################################################################################################################
from python_language.programming_languages_python.fourteenth_laba_lang.classes import *

ENV = Env()
ENV.read_env()


def generate_table(array: np.ndarray) -> PrettyTable:
    """
    Функция, которая создает таблицу, служит интерфейсом для генерации таблицы.
    :param array: Массив, который мы хотим поместить в нашу таблицу.
    :return: Таблица с исходными данными.
    """
    table = PrettyTable()

    match type(array[0]).__name__:
        case "Student":
            table.field_names = ["Фамилия", "Инициалы", "Номер группы", "Оценки", "Средний балл"]
            _generate_table_students(table=table, students=array)

        case "Train":
            table.field_names = ["Номер поезда", "Пункт назначения", "Время отправления"]
            _generate_table_trains(table=table, trains=array)

    return table


def _generate_table_students(table: PrettyTable, students: np.ndarray) -> None:
    """
    Функция, которая печатает таблицу со студентами.
    :param table: Таблица, которая будет использоваться для заполнения.
    :param students: Все студенты, которых мы хотим добавить в таблицу.
    """
    # создаем массив со средними баллами, чтобы можно было сделать сортировку
    sorting_key = [np.mean(student.grades) for student in students]
    # получаем индексы, как мы будем сортировать (по умолчанию идет по возрастанию
    sorting_indexes = np.argsort(sorting_key)
    # добавляем в таблицу все наши значения
    table.add_rows(
        [
            student.last_name,
            student.initials,
            student.number_group,
            ', '.join(map(str, student.grades)),
            np.mean(student.grades).round(3)
        ]
        for student in students[sorting_indexes]
    )


def _generate_table_trains(table: PrettyTable, trains: np.ndarray) -> None:
    """
    Функция, которая печатает таблицу с поездами.
    :param table: Таблица, которая будет использоваться для заполнения.
    :param trains: Все поезда, которые мы хотим добавить в таблицу
    """
    table.add_rows([train.number, train.dest, train.departure] for train in trains)


def generate_subscriber() -> Subscriber:
    """
    Функция, которая генерирует абонента для заполнения в массив
    :return: возвращает подписчика.
    """
    # Генерируется русское имя в формате ИОФ
    person = RussianNames().get_person().split()

    return Subscriber(
        identification_number=np.random.randint(1000, 9999),
        surname=person[2],
        first_name=person[0],
        patronymic=person[1],
        address=Address(Locale.RU).address(),
        credit_card_number=np.random.randint(1000, 9999),
        debit=np.random.uniform(1000, 10000),
        credit=np.random.uniform(0, 5000),
        intercity_call_time=Datetime().time().replace(microsecond=0),
        local_call_time=Datetime().time().replace(microsecond=0))


def generate_buyer() -> Buyer:
    """
    Функция, которая генерирует покупателя для заполнения в массив
    :return: возвращает покупателя.
    """
    # Генерируется русское имя в формате ИОФ
    person = RussianNames().get_person().split()

    return Buyer(
        name=person[0],
        patronymic=person[1],
        surname=person[2],
        address=Address(Locale.RU).address(),
        credit_card_number=int(RussiaSpecProvider().kpp()) // 100,
        bank_account_number=int(RussiaSpecProvider().bic()) // 100
    )


def generate_student() -> Student:
    """
    Функция, которая генерирует студента.
    :return: Возвращает студента.
    """
    # Генерируется русское имя в формате ИОФ
    person = RussianNames().get_person().split()

    return Student(
        last_name=person[2],
        initials=f"{person[0][0]}.{person[1][0]}",
        number_group=np.random.randint(1, 10),
        grades=np.random.uniform(2.0, 5.0, 5).round(2)
    )


def generate_train(number: int) -> Train:
    """
    Функция, которая генерирует поезд.
    :param number: Номер поезда.
    :return: Возвращает поезд.
    """
    # генерируем случайный адрес куда отправится наш поезд в России
    destination = Address(Locale.RU)
    return Train(
        dest=f"{destination.federal_subject()} г.{destination.city()}",
        number=number,
        departure=Datetime().time().replace(microsecond=0)
    )


def generate_book() -> Book:
    """
    Функция, которая создает книжку.
    :returns: Возвращает случайную книгу.
    """
    # тут запрос идет к API, который генерирует случайные книги
    books = requests.get("http://titlegen.us-east-1.elasticbeanstalk.com/api/v1/titlegen?type=song&no=4").json()['data']

    return Book(
        title=random.choice(books),
        author=RussianNames().get_person(),
        year=Datetime().year()
    )


def generate_animal(identifier: int) -> Herbivore | Omnivore | Carnivore:
    """
    Функция, которая генерирует случайное животное. Здесь идет запрос к одному сайту, где находится список животных.
    После этого передается api ninjas для генерации фактов о данном животном, дальше идет только ручной парсинг данных.
    Работает достаточно медленно из-за requests. В асинхронном стиле писать все не хочется ради этого...
    :param identifier: Идентификатор животного.
    :returns: Возвращает животное
    """
    dictionary = {"Herbivore": Herbivore,
                  "Omnivore": Omnivore,
                  "Carnivore": Carnivore}

    while True:
        # делаем запрос, чтобы получить список с животными
        animals = requests.get('http://davidbau.com/data/animals').text.strip().splitlines()
        #
        random_animal = random.choice(animals)

        res = requests.get(f"https://api.api-ninjas.com/v1/animals?name={random_animal}",
                           headers={'X-Api-Key': ENV('ANIMALS')})

        if res.status_code != 200:
            raise Exception(f"Вы не добавили в env файл API_ANIMALS с сайта api-ninjas")

        if data := res.json():
            return dictionary[data[0]["characteristics"]["diet"]](identifier=identifier, name=random_animal)


def write_to_file(animals: list[Animal]) -> None:
    """
    Функция, которая записывает всех животных в json файл для сохранения
    """
    with open('animals.json', 'w', encoding="utf-8") as f:
        json.dump(animals, f, default=Animal.animal_to_dict, indent=4, ensure_ascii=False)


def read_from_file() -> list[Animal]:
    """
    Функция, которая считывает данные о животных с файла
    """
    with open('animals.json', 'r', encoding="utf-8") as f:
        return json.loads(f.read(), object_hook=Animal.dict_to_animal)
