import re


def increase_age_by_name(data: dict, s: str) -> dict:
    """
    Увеличить возраст конкретного студента на какое-то число.
    Пример ввода: Изменить возраст Dwain Huff на 3
    """
    person = re.search(r"\b[A-Za-z]+\s[A-Za-z]+\b", s).group(0)
    number_age = int(re.search(r'\d+', s).group(0))
    for key, value in data.items():
        if value[0] == person:
            value[1] = int(value[1]) + number_age
            return {key: value}


def change_name(data: dict, s: str) -> dict:
    """
    Изменить ФИО студента.
    Пример ввода: изменить ФИО студента с Dwain Huff на Pavel Slesarenko
    """
    who_to_change, to_whom_to_change = re.findall(r'\b[A-Za-z]+\s[A-Za-z]+\b', s)
    for key, value in data.items():
        if value[0] == who_to_change:
            value[0] = to_whom_to_change
            return {key: value}


def increase_age_by_number(data: dict, s: str) -> dict:
    """
    Увеличить возраст студента по номеру.
    Пример ввода: увеличить возраст студента под номером №1 на 8
    """
    number_person, number_age = re.findall(r"\b№\d+\b|\d+", s)
    for key, value in data.items():
        if key == number_person:
            value[1] = int(value[1]) + abs(int(number_age))
            return {key: value}


def change_group_by_name(data: dict, s: str) -> dict:
    """
    Изменить группу студента. Поиск по ФИО.
    Пример ввода: изменить группу студента Phil Bowman на ВКБ - 22
    """
    person = re.search(r"\b[A-Za-z]+\s[A-Za-z]+\b", s).group(0)
    new_group = re.search(r'[a-zA-Zа-яА-ЯёЁ]+ - \d+', s).group(0)
    for key, value in data.items():
        if value[0] == person:
            value[-1] = new_group
            return {key: value}


def delete_student_by_number(data: dict, s: str) -> dict | str:
    """
    Удалить запись о студенте. Поиск по №
    """
    try:
        if data.pop(re.search(r"\d+", s).group(0)):
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
        lst = value[0].split()
        if lst[1] == "Иванов":
            lst[1] = "Сидоров"
            value[0] = ' '.join(lst)
    return data


def swap_places(data: dict, s=None) -> dict:
    """
    Поменять ФИО и Группа местами
    """
    for key, value in data.items():
        value[0], value[2] = value[2], value[0]
    return data
