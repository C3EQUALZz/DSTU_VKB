from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from db_creation.tables import Teacher, Department, Position

engine = create_engine('sqlite:///database.db', echo=False)
session = sessionmaker(bind=engine)()

__all__ = [
    "remove_by_position", "remove_by_name", "remove_by_department",
    "add_new_position", "add_new_department", "add_new_teacher",
]


def remove_by_name(data: tuple[str, ...]) -> bool:
    """
    Удаляет по имени преподавателя
    Args:
        data[tuple[str]] - переменное количество аргументов, здесь мне нужно будет только имя
    Пример ввода: удалить преподавателя Роман Лапина (постоянно меняется значение)
    """
    name_to_delete = data[-1]
    teacher_to_delete = session.query(Teacher).filter_by(name=name_to_delete).first()
    if teacher_to_delete:
        session.delete(teacher_to_delete)
        session.commit()
        return True


def remove_by_department(data: tuple[str, ...]) -> bool:
    """
    Удаляет всех по названию кафедры
    Args:
        data[tuple[str]] - переменное количество аргументов, здесь мне нужно будет всех, кто с определенной кафедры
    Пример ввода: удалить всех с кафедры КБИС
    """
    department_to_delete = data[-1]
    # Получаем объект кафедры из базы данных
    if department := session.query(Department).filter_by(title=department_to_delete).first():
        # Получаем всех преподавателей, связанных с кафедрой
        teachers_to_delete = session.query(Teacher).filter_by(department_id=department.id).all()

        # Удаляем каждого преподавателя
        for teacher in teachers_to_delete:
            session.delete(teacher)

        # Удаляем саму кафедру
        session.delete(department)
        # Зафиксировать изменения в базе данных
        session.commit()
        return True


def remove_by_position(data: tuple[str, ...]) -> bool:
    """
    Удаляет всех, кто находится на данной должности
    Args:
        data[tuple[str]] - переменное количество аргументов, здесь мне нужно те, кого удалить по определенной должности
    """
    position_to_delete = data[-1]
    # Получаем объект должности из базы данных
    if position := session.query(Position).filter_by(title=position_to_delete).first():
        # Получаем всех преподавателей, связанных с должностью
        teachers_to_delete = session.query(Teacher).filter_by(depatment_id=position.id).all()
        # Удаляем каждого преподавателя
        for teacher in teachers_to_delete:
            session.delete(teacher)
        # Удаляем полностью должность
        session.delete(position)
        # Сохраняем изменения
        session.commit()
        return True


def add_new_position(data: tuple[str, ...]) -> bool:
    """
    Метод, который добавляет новую должность преподавателя
    Args:
        data[tuple[str]] - переменное количество аргументов, здесь мне нужно будет извлечь должность
    """
    


def add_new_department():
    ...


def add_new_teacher():
    ...
