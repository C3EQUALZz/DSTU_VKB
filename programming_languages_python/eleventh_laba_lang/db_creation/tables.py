"""
Здесь описывается логика таблиц. Каждый из классов - это просто таблица
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# используется для декларативного стиля, явно не будем связывать с БД, как я понял
Base = declarative_base()


class Position(Base):
    """
    Класс, который описывает должность учителей
    """
    # название таблицы
    __tablename__ = 'positions'
    # 1 колонка - целое число, является первичным ключом
    id: int = Column(Integer, primary_key=True)
    # 2 колонка - строка, здесь будет просто должность относительно id
    title: str = Column(String)


class Department(Base):
    """
    Класс, который описывает кафедру
    """
    # название таблицы
    __tablename__ = 'departments'
    # 1 колонка - целое число, первичный ключ
    id: int = Column(Integer, primary_key=True)
    # название кафедры
    title: str = Column(String(25))
    # название института
    institute: str = Column(String(50))


class Teacher(Base):
    """
    Класс, который описывает учителя
    """
    # название таблицы
    __tablename__ = 'teachers'
    # первичный ключ
    id: int = Column(Integer, primary_key=True)
    # ФИО преподавателя
    name: str = Column(String(50))
    # Возраст преподавателя
    age: int = Column(Integer)
    # ID кафедры, здесь мы ставим относительно какого внешнего ключа тут идет связь
    department_id: int = Column(Integer, ForeignKey('departments.id'))
    # ID должности
    position_id: int = Column(Integer, ForeignKey('positions.id'))




