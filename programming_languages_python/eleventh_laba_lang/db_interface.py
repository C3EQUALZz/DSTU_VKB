from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from db_creation.tables import Teacher, Department

engine = create_engine('sqlite:///database.db', echo=False)
session = sessionmaker(bind=engine)()

__all__ = [
    "remove_by_position", "remove_by_name", "remove_by_department",
    "add_new_position", "add_new_department", "add_new_teacher",
]


def remove_by_name(name_to_delete: str) -> bool:
    """
    Удаляет по имени преподавателя
    Args:
        name_to_delete[str]: имя преподавателя, которого мы хотим удалить
    """
    teacher_to_delete = session.query(Teacher).filter_by(name=name_to_delete).first()
    if teacher_to_delete:
        session.delete(teacher_to_delete)
        session.commit()
        return True


def remove_by_department(department_to_delete: str) -> bool:
    """
    Удаляет всех по названию кафедры
    Args:

    """
    # Получаем объект кафедры из базы данных
    if department := session.query(Department).filter_by(title=department_to_delete).first():
        # Получаем всех преподавателей связанных с кафедрой
        teachers_to_delete = session.query(Teacher).filter_by(department_id=department.id).all()

        # Удаляем каждого преподавателя
        for teacher in teachers_to_delete:
            session.delete(teacher)

        # Удаляем саму кафедру
        session.delete(department)
        # Зафиксировать изменения в базе данных
        session.commit()
        return True


def remove_by_position():
    ...

def add_new_position():
    ...

def add_new_department():
    ...

def add_new_teacher():
    ...
