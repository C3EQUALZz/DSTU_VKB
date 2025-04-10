import os

########################################################################################################################
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

########################################################################################################################
from .db_creation.tables import Department, Position, Teacher

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

engine = create_engine(f"sqlite:///{file_path}", echo=False)
session = sessionmaker(bind=engine)()

__all__ = [
    "remove_by_position",
    "remove_by_name",
    "remove_by_department",
    "add_new_position",
    "add_new_department",
    "add_new_teacher",
    "change_teacher_name",
    "change_department",
]


def remove_by_name(data: tuple[str, ...]) -> bool:
    """
    Функция, которая удаляет по имени преподавателя
    Args:
        data[tuple[str]] - переменное количество аргументов, здесь мне нужно будет только имя
    Пример ввода: удалить преподавателя Роман Лапина (постоянно меняется значение)
    """
    name_to_delete = data[-1].strip().title()
    teacher_to_delete = session.query(Teacher).filter_by(name=name_to_delete).first()
    if teacher_to_delete:
        session.delete(teacher_to_delete)
        session.commit()
        return True


def remove_by_department(data: tuple[str, ...]) -> bool:
    """
    Функция, которая удаляет всех по названию кафедры
    Args:
        data[tuple[str]] - информация после match.groups(), здесь мне нужно будет взять всех, кто с определенной кафедры
    Пример ввода: удалить всех с кафедры КБИС
    """
    department_to_delete = data[-1].strip()
    # Получаем объект кафедры из базы данных
    if (
        department := session.query(Department)
        .filter_by(title=department_to_delete)
        .first()
    ):
        # Получаем всех преподавателей, связанных с кафедрой
        teachers_to_delete = (
            session.query(Teacher).filter_by(department_id=department.id).all()
        )

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
    Функция, которая удаляет всех, кто находится на данной должности
    Args:
        data[tuple[str]] - информация после match.groups(), здесь мне нужны те, кого удалить по определенной должности
    Пример ввода: удалить всех, кто имеет звание - Декан
    """
    position_to_delete = data[-1].strip().title()
    # Получаем объект должности из базы данных
    if position := session.query(Position).filter_by(title=position_to_delete).first():
        # Получаем всех преподавателей, связанных с должностью
        teachers_to_delete = (
            session.query(Teacher).filter_by(position_id=position.id).all()
        )
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
    Функция, которая добавляет новую должность преподавателя
    Args:
        data[tuple[str]] - переменное количество аргументов, здесь мне нужно будет извлечь должность
    Пример: Добавить новое звание - ректор
    """
    position_to_add = data[-1].strip().capitalize()
    # Если уже существует в таблице, то мы добавлять не будем
    if session.query(Position).filter_by(title=position_to_add).first():
        return True

    # Добавляем новую должность, если все-таки не было в таблице
    new_position = Position(title=position_to_add)
    session.add(new_position)
    session.commit()
    return True


def add_new_department(data: tuple[str, ...]) -> bool:
    """
    Метод, который добавляет новую кафедру
    Args:
        data[tuple[str]] - информация после match.groups(), здесь я беру названия кафедры
    Пример: добавить новую кафедру ФИИТ в университет SFEDU
    """
    department_to_add, university = map(lambda x: x.strip().capitalize(), data[-2:])
    # Если уже существует в таблице, то мы добавлять не будем
    if (
        session.query(Department)
        .filter_by(title=department_to_add, institute=university)
        .first()
    ):
        return True

    # Добавляем новую кафедру, если все-таки не было в таблице
    new_department = Department(title=department_to_add, institute=university)
    session.add(new_department)
    session.commit()
    return True


def add_new_teacher(data: tuple[str, ...]) -> bool:
    """
        Метод, который добавляет нового преподавателя
        Args:
             data[tuple[str]] - информация после match.groups(), здесь мы берем все данные,
             которые ввел пользователь, про преподавателя
        Пример:
    Добавить нового преподавателя Эльмира Рафаиловна с возрастом 20 на кафедру КБИС в университет DSTU на должность старший преподаватель
    """
    name, age, department_title, institute, position_title = map(
        str.title, map(str.strip, data[-5:])
    )
    department_title, institute = map(str.upper, (department_title, institute))

    # находим ID кафедры относительно названия
    department_id = (
        session.query(Department.id)
        .filter_by(title=department_title, institute=institute)
        .first()
    )
    if department_id is None:
        new_department = Department(title=department_title, institute=institute)
        session.add(new_department)
        session.commit()

    # находим ID звания относительно названия
    position_id = session.query(Position.id).filter_by(title=position_title).first()
    if position_id is None:
        new_position = Position(title=position_title)
        session.add(new_position)
        session.commit()

    # Если существует уже данный преподаватель, то не добавляем его в БД
    if (
        session.query(Teacher)
        .filter_by(
            name=name,
            age=age,
            department_id=department_id[0],
            position_id=position_id[0],
        )
        .scalar()
    ):
        return True

    new_teacher = Teacher(
        name=name, age=age, department_id=department_id[0], position_id=position_id[0]
    )
    session.add(new_teacher)
    session.commit()
    return True


def change_teacher_name(data: tuple[str, ...]) -> bool:
    """
    Меняет имя преподавателя
    Args:
        data[tuple[str]] - здесь мне нужно будет взять имя нового преподавателя, ещё в аргументах будет прошлое
    """
    old_name, new_name = map(str.strip, data[-2:])

    if teacher_to_replace := session.query(Teacher).filter_by(name=old_name).first():
        print(teacher_to_replace)
        teacher_to_replace.name = new_name
        session.commit()
        return True


def change_department(data: tuple[str, ...]) -> bool:
    """
    Меняет название кафедры
    Args:
        data[tuple[str]] - здесь будут лежать названия кафедр
    """
    old_name, new_name = map(str.strip, data[-2:])

    if (
        department_to_replace := session.query(Department)
        .filter_by(title=old_name)
        .first()
    ):
        department_to_replace.title = new_name
        session.commit()
        return True
