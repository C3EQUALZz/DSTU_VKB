"""
Здесь описывается логика таблиц. Каждый из классов - это просто таблица
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

__all__ = ["Country", "City", "Street", "Base"]

# используется для декларативного стиля, явно не будем связывать с БД, как я понял
Base = declarative_base()


class Country(Base):
    """
    Класс, который описывает страну
    """
    # название таблицы
    __tablename__ = 'countries'
    # id таблицы
    id = Column(Integer, primary_key=True)
    # название страны
    title = Column(String(50))
    # id города
    city_id = Column(Integer, ForeignKey('cities.id'))


class City(Base):
    """
    Класс, который описывает город
    """
    # название таблицы
    __tablename__ = 'cities'
    #
    id = Column(Integer, primary_key=True)
    name = Column(String(25))


class Street(Base):
    """
    Класс, который описывает улицу
    """
    # название таблицы
    __tablename__ = 'streets'
    # id таблицы
    id = Column(Integer, primary_key=True)
    # имя улицы
    name = Column(String(50))
    # id города
    city_id = Column(Integer, ForeignKey('cities.id'))
