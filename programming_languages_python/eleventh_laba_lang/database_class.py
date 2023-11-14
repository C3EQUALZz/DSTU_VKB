"""
Здесь описан сам класс, который используется для подключения к БД
Здесь реализован паттерн Singleton, здесь используется контекстный менеджер для закрытия БД
"""
import sqlite3


class Database:
    """
    Контекстный менеджер для управления с БД
    """
    inheritance = None

    def __new__(cls, database_name):
        if Database.inheritance is None:
            Database.inheritance = sqlite3.connect(database_name)
        return Database.inheritance

    def __enter__(self):
        return Database.inheritance

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            Database.inheritance.rollback()
        else:
            Database.inheritance.commit()
        Database.inheritance.close()
