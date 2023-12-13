from mimesis import Address
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .tables import Base, Country, City, Street


class DatabaseManager:
    def __init__(self, engine):
        self.engine = engine
        self.Base = Base
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self) -> None:
        self.Base.metadata.create_all(self.engine)

    def populate_data(self, fill_function) -> None:
        with self.Session() as session:
            fill_function(session)
            session.commit()


def fill_random_data(session: Session) -> None:
    generic = Address()
    countries = [Country(name=generic.country()) for _ in range(3)] + [Country(name="Albania"), Country(name="РФ")]
    cities = [City(name=generic.city(), country=countries[i % 5]) for i in range(5)]
    streets = [Street(name=generic.street_name(), city=cities[i % 5]) for i in range(57)]

    session.add_all(countries + cities + streets)


def create_database(path) -> None:
    engine = create_engine(f"sqlite:///{path}", echo=False)
    db_manager = DatabaseManager(engine)
    db_manager.create_tables()
    db_manager.populate_data(fill_random_data)
