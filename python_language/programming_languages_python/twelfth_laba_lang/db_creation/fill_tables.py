from random import randint
from typing import Callable

########################################################################################################################
from mimesis import Address
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

########################################################################################################################
from .tables import Base, Country, City, Street


class DatabaseManager:
    def __init__(self, engine: Engine):
        # Абстракция для подключения к БД
        self.engine = engine
        self.Base = Base
        # интерфейс для взаимодействия с БД
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self) -> None:
        """
        Здесь создаются наши таблицы неявно, декларативный подход.
        Изначально в файле tables я инициализировал каждую таблицу, наследуясь от Base.
        Теперь здесь происходит создание
        """
        self.Base.metadata.create_all(self.engine)

    def populate_data(self, fill_functions: Callable[[Session], None]):
        """
        Метод, который заполняет нашу БД случайными данными
        """
        # контекстный менеджер сохранение не делает, такая реализация в классе Session
        with self.Session() as session:
            fill_functions(session)
            session.flush()
            session.commit()

    @staticmethod
    def fill_countries(session: Session) -> None:
        """
        Метод, который заполняет страны в нашей таблице
        """
        fake = Address()

        for _ in range(25):
            country = Country(title=fake.country(), city_id=randint(1, 25))
            session.add(country)

    @staticmethod
    def fill_cities(session: Session) -> None:
        """
        Метод, который добавляет города в базу данных
        """
        fake = Address()
        for _ in range(25):
            city = City(name=fake.city())
            session.add(city)

    @staticmethod
    def fill_streets(session: Session) -> None:
        """
        Метод, который добавляет города в базу данных
        """
        fake = Address()
        for _ in range(25):
            street = Street(name=fake.street_name(), city_id=randint(1, 25))
            session.add(street)


def create_database() -> None:
    # подключение к БД
    engine = create_engine('sqlite:///database.db', echo=False)
    # Передаем нашей БД для создания таблиц и значений
    db_manager = DatabaseManager(engine)
    db_manager.create_tables()

    db_manager.populate_data(DatabaseManager.fill_countries)
    db_manager.populate_data(DatabaseManager.fill_cities)
    db_manager.populate_data(DatabaseManager.fill_streets)
