import re


def extract_info(s: str):
    """
    Вспомогательная функция для нахождения имени человека, возраста, на кого заменить
    """
    person = re.search(r'\b[A-Za-z]+\s[A-Za-z]+\b', s).group(0)
    number_age = int(re.search(r'\d+', s).group(0))
    to_whom_to_change = re.search(r'\b[A-Za-z]+\s[A-Za-z]+\b', s)

    return person, number_age, to_whom_to_change


def increase_age_by_name(data: dict, s: str) -> dict:
    """
    Увеличить возраст конкретного студента на какое-то число.
    Пример ввода: Изменить возраст Dwain Huff на 3
    """
    person, number_age, _ = extract_info(s)
    for key, value in data.items():
        if value[0] == person:
            value[1] = int(value[1]) + number_age
            return {key: value}


def change_name(data: dict, s: str) -> dict:
    """
    Изменить ФИО студента.
    Пример ввода: изменить ФИО студента с Dwain Huff на Pavel Slesarenko
    """
    who_to_change, to_whom_to_change, _ = extract_info(s)
    for key, value in data.items():
        if value[0] == who_to_change:
            value[0] = to_whom_to_change
            return {key: value}


def increase_age_by_number(data: dict, s: str) -> dict:
    """
    Увеличить возраст студента по номеру.
    Пример ввода: увеличить возраст студента под номером №1 на 8
    """
    number_person, number_age, _ = extract_info(s)
    for key, value in data.items():
        if key == number_person:
            value[1] = int(value[1]) + abs(number_age)
            return {key: value}


def change_group_by_name(data: dict, s: str) -> dict:
    """
    Изменить группу студента. Поиск по ФИО.
    """
    person, _, new_group = extract_info(s)
    for key, value in data.items():
        if value[0] == person:
            value[-1] = new_group
            return {key: value}


def delete_student_by_number(data: dict, s: str) -> dict | str:
    """
    Удалить запись о студенте. Поиск по №
    """
    try:
        if data.pop(re.search(r"\d+", s)):
            return data
    except KeyError:
        return "Нет такого ключа"


def decrease_age_if_more_than_22(data: dict, s=None) -> dict:
    """
    Если возраст студента больше 22 уменьшить его на 1
    """
    for key, value in data.items():
        if int(value[1]) > 22:
            value[1] = int(value[1]) - 1
    return data


def delete_student_if_age_eq_23(data: dict, s=None) -> dict:
    """
    Если возраст студента равен 23, удалить его из списка
    """
    return {x: data[x] for x in data if int(data[x][1]) != 23}


def increase_if_surname_ivanov(data: dict, s=None) -> dict:
    """
    У всех студентов с фамилией Иванов увеличить возраст на 1
    """
    for key, value in data.items():
        if value[0].split()[1] == "Иванов":
            value[1] = int(value[1]) + 1
    return data


def change_ivanov_sidorov(data: dict, s=None) -> dict:
    """
    У студентов с фамилией Иванов изменить фамилию на Сидоров
    """
    for key, value in data.items():
        if (lst := value[0]).split()[1] == "Иванов":
            lst[1] = "Сидоров"
            value[0] = ' '.join(lst)
    return data


def swap_places(data: dict) -> dict:
    """
    Поменять ФИО и Группа местами
    """
    for key, value in data.items():
        value[0], value[1] = value[1], value[0]
    return data
