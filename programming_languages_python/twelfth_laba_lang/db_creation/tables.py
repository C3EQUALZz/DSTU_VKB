"""
Здесь описывается логика таблиц. Каждый из классов - это просто таблица
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

__all__ = ["Country", "City", "Street", "Base"]

# используется для декларативного стиля, явно не будем связывать с БД, как я понял
Base = declarative_base()


class Country(Base):
    """
    Класс, который описывает страну
    """

    # название таблицы
    __tablename__ = "countries"
    # id таблицы
    id = Column(Integer, primary_key=True)
    # название страны
    name = Column(String(50), nullable=False)
    # id города
    cities = relationship("City", back_populates="country")


class City(Base):
    """
    Класс, который описывает город
    """

    # название таблицы
    __tablename__ = "cities"
    #
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"))
    streets = relationship("Street", back_populates="city")
    country = relationship("Country", back_populates="cities")


class Street(Base):
    """
    Класс, который описывает улицу
    """

    # название таблицы
    __tablename__ = "streets"
    # id таблицы
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"))
    city = relationship("City", back_populates="streets")
