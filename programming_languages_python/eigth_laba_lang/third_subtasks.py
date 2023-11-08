def print_by_group(data: dict) -> dict:
    """
    Вывести список студентов группы БО - 111111
    """
    return {x: data[x] for x in data if data[x][-1] == "БО - 111111"}


def print_by_numbers(data: dict) -> dict:
    """
    Вывести список студентов с номерами от 1 до 10
    """
    return {x: data[x] for x in data if 1 <= int(x) <= 10}


def print_by_age(data: dict) -> dict:
    """
    Списка студентов в возрасте 22 лет
    """
    return {x: data[x] for x in data if data[x][1] == 22}


def print_by_surname(data: dict) -> dict:
    """
    Список студентов с фамилией Иванов
    """
    return {x: data[x] for x in data if data[0].split()[1] == "Иванов"}


def print_by_surname_end_a(data: dict) -> dict:
    """
    Списка студентов, чьи фамилии заканчиваются на 'a'
    """
    return {x: data[x] for x in data if data[0].split()[1].endswith("a")}


def print_by_age_even(data: dict) -> dict:
    """
    Список студентов, чей возраст - это четное число
    """
    return {x: data[x] for x in data if int(data[x][1]) % 2 == 0}


def print_by_age_if_5(data: dict) -> dict:
    """
    Список студентов, если в возрасте студента встречается число 5
    """
    return {x: data[x] for x in data if '5' in data[x][1]}


def print_by_length_group(data: dict) -> dict:
    """
    Список студентов, если их номера группы длиннее 7 символов
    """
    return {x: data[x] for x in data if len(data[x][-1]) > 7}


def print_by_even_number(data: dict) -> dict:
    """
    Список студентов (а также информацию о них), если их № - четное число
    """
    return {x: data[x] for x in data if int(x) % 2 == 0}


def print_by_group_ends_1(data: dict) -> dict:
    """
    Список студентов, если их номер группы заканчивается на '1'
    """
    return {x: data[x] for x in data if data[x][-1].endswith("1")}

