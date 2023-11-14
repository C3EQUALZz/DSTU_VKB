"""
Модуль создан с той целью, чтобы пользователь здесь заполнял все данные
"""

import sqlite3

from programming_languages_python.eleventh_laba_lang.database_class import Database

END_OF_FILLING: tuple[str, ...] = ("конец", "все", "end", "exit", "e")


def create_database() -> sqlite3.Connection:
    """
    Создает столбцы для базы данных.
    Мой контекстный менеджер сам создает файл. Подробнее смотрите в database_class
    """
    with Database("server-dstu.db") as db:
        cursor = db.cursor()
        cursor.executescript("""
        PRAGMA foreign_keys=ON;

         CREATE TABLE IF NOT EXISTS Должность 
         (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Название TEXT
         );

         CREATE TABLE IF NOT EXISTS Кафедра
         (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Название TEXT UNIQUE,
            Институт TEXT
        );

        CREATE TABLE IF NOT EXISTS Преподаватель
         (
            id INTEGER AUTOINCREMENT,
            ФИО TEXT UNIQUE,
            Возраст INTEGER,
            ID_Кафедры INTEGER ,
            ID_Должности,
            FOREIGN KEY (ID_Кафедры) REFERENCES Кафедра (id),
            FOREIGN KEY (ID_Должности) REFERENCES Должность (id)
         );

        """)
    return db


def fill_table(db: sqlite3.Connection, table_name: str):
    """
    Функция для заполнения таблицы из терминала.
    Работает до того момента, пока не будет введено любое значение из END_OF_FILLING
    """
    cursor, description = db.cursor(), f"Введите данные для таблицы {table_name} (или введите 'все' для завершения): "

    while (user_input := input(description).strip()).lower() not in END_OF_FILLING:
        # Предполагается, что пользователь вводит данные через запятую
        data = user_input.split(', ')
        # Безопасная вставка через '?', позволяет избежать SQL Injection
        cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['?'] * len(data))})", data)
        db.commit()


def fill_database():
    database = create_database()

    description: str = "Введите название таблицы, значения которой хотите заполнять. В ином случае напишите 'Конец'. "
    while (table := input(description).strip()).lower() not in END_OF_FILLING:
        fill_table(db=database, table_name=table)
