from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
########################################################################################################################
from .tables import Base, Teacher, Position, Department
########################################################################################################################
from mimesis import Generic, Locale
from typing import Callable

__all__ = ["create_database"]


class DatabaseManager:
    def __init__(self, engine):
        # Абстракция для подключения к БД
        self.engine = engine
        self.Base = Base
        # интерфейс для взаимодействия с БД
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self) -> None:
        """
        Здесь создаются наши таблицы неявно, декларативный подход
        """
        self.Base.metadata.create_all(self.engine)

    @staticmethod
    def fill_positions(session: Session) -> None:
        positions_data = ('Декан', 'Заместитель декана',
                          'Заведующий кафедрой', 'Старший преподаватель',
                          'Ассистент', 'Лаборант', 'Доцент', 'Профессор')
        for title in positions_data:
            position = Position(title=title)
            session.add(position)

    @staticmethod
    def fill_departments(session: Session) -> None:
        departments_data = (
            {'title': 'Высшая математика', 'institute': 'DSTU'},
            {'title': 'Прикладная математика', 'institute': 'DSTU'},
            {'title': 'ПОВТиАС', 'institute': 'DSTU'},
            {'title': 'КБИС', 'institute': 'DSTU'},
            {'title': 'Информатика и математика', 'institute': 'DSTU'},
            {'title': 'ВСиИБ', 'institute': 'DSTU'},
            {'title': 'Алгебра и дискретная математика', 'institute': 'SFEDU'},
            {'title': 'Вычислительная математика и математическая физика', 'institute': 'SFEDU'},
            {'title': 'Информатика и вычислительный эксперимент', 'institute': 'SFEDU'}
        )
        for department_data in departments_data:
            department = Department(**department_data)
            session.add(department)

    @staticmethod
    def fill_teachers(session: Session) -> None:
        fake = Generic(Locale.RU)

        for _ in range(10):
            teacher = Teacher(
                name=fake.person.full_name(),
                age=fake.random.randint(25, 65),
                department_id=fake.random.randint(1, 4),
                position_id=fake.random.randint(1, 4),
            )
            session.add(teacher)

    def populate_data(self, fill_functions: Callable[[Session], None]):
        """
        Метод, который заполняет нашу БД случайными данными
        """
        with self.Session() as session:
            fill_functions(session)
            session.flush()
            session.commit()


def create_database() -> None:
    # подключение к БД
    engine = create_engine('sqlite:///database.db', echo=False)
    # Передаем нашей БД для создания таблиц и значений
    db_manager = DatabaseManager(engine)
    db_manager.create_tables()

    db_manager.populate_data(DatabaseManager.fill_positions)
    db_manager.populate_data(DatabaseManager.fill_departments)
    db_manager.populate_data(DatabaseManager.fill_teachers)
