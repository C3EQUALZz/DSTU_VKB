"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""

__all__ = [
    "first_question",
    "second_question",
    "third_question",
    "fourth_question",
    "fifth_question",
    "sixth_question",
    "seventh_question",
]

import re
from functools import partial
from pprint import pprint

########################################################################################################################
import arrow
import numpy as np
from prettytable import PrettyTable
########################################################################################################################
from python_language.programming_languages_python.fourteenth_laba_lang.classes import *
from python_language.programming_languages_python.fourteenth_laba_lang.help_functions import *


def first_question(what_to_do: str) -> PrettyTable | str:
    """
    Создать класс Student, содержащий поля: фамилия и инициалы, номер группы, успеваемость (массив из пяти элементов).
    Создать массив из десяти элементов такого типа, упорядочить записи по возрастанию среднего балла.
    Добавить возможность вывода фамилий и номеров групп студентов, имеющих оценки, равные только 4 или 5.
    """
    # mimesis не поддерживает отчества, так как в английском их нет, поэтому такая затычка будет.
    students: np.ndarray[Student, ...] = np.array(
        [generate_student() for _ in range(10)]
    )

    if re.fullmatch(
        "Вывести всех студентов имеющих только оценки 4 или 5", what_to_do.strip()
    ):
        students = np.array(
            [
                student
                for student in students
                if all(grade in (4.0, 5.0) for grade in student.grades)
            ]
        )

        if students.size == 0:
            return "Нет таких учеников"

    return generate_table(students)


def second_question(what_to_do: str) -> str | PrettyTable:
    """
    Создать класс с именем Train, содержащий поля: название пункта назначения, номер поезда, время отправления.
    Ввести данные в массив из пяти элементов типа train, упорядочить элементы по номерам поездов.
    Добавить возможность вывода информации о поезде, номер которого введен пользователем.
    Добавить возможность сортировки массива по пункту назначения, причем поезда с одинаковыми пунктами назначения
    должны быть упорядочены по времени отправления.
    """
    list_trains = np.array([generate_train(number) for number in range(1, 6)])

    trains = Trains(trains=list_trains)

    if reg := re.fullmatch(
        r"^Вывести информацию о поезде под номером (\d+)$", what_to_do.strip(), re.I
    ):
        return trains[trains.find(int(reg.group(1)))].info

    if re.fullmatch(
        r"^Отсортировать поезда по пункту назначения|Отсортировать$",
        what_to_do.strip(),
        re.I,
    ):
        trains.sort(lambda train: (train.dest, train.departure))
        return generate_table(trains.trains)

    if re.fullmatch(
        r"^Вывести всю таблицу расписания поездов$", what_to_do.strip(), re.I
    ):
        return generate_table(trains.trains)

    return "Вы неправильно ввели"


def third_question(string: str):
    """
    Создать класс с двумя переменными.
    Добавить функцию вывода на экран и функцию изменения этих переменных.
    Добавить функцию, которая находит сумму значений этих переменных.
    Функцию, которая находит наибольшее значение из этих двух переменных.
    """
    if res := re.fullmatch(
        r"^Найти сумму значений (?:переменных)?(\d+) (\d+)$", string.strip(), re.I
    ):
        var = TwoVariables(*map(int, res.groups()))
        return var.sum()

    if res := re.fullmatch(
        r"^Найти наибольшее значение (\d+) (\d+)$", string.strip(), re.I
    ):
        var = TwoVariables(*map(int, res.groups()))
        return var.max_variable()

    if res := re.fullmatch(
        r"^Изменить переменные с (\d+ \d+) на (\d+ \d+)$", string.strip(), re.I
    ):
        var = TwoVariables(*map(int, res.group(1).split()))
        return var.modify(*map(int, res.group(2).split()))


def fourth_question(what_to_do: str):
    """
    Класс «Домашняя библиотека». Предусмотреть возможность работы с произвольным числом книг, поиска книги по
    какому-либо признаку (например, по автору или по году издания), добавления книг в библиотеку,
    удаления книг из нее, сортировки книг по разным полям.
    Пример ввода: Добавить книгу Ульрика-в-Торгейте Королёв И.А 2021
    Пример ввода: Удалить книгу Муму Тургенев Иван Сергеевич 1852
    Пример ввода: Найти книгу по автору - Тургенев Иван Сергеевич
    """
    books = [generate_book() for _ in range(5)] + [
        Book(title="Муму", author="Тургенев Иван Сергеевич", year=1852)
    ]

    library = Library(books=books)

    patterns: list = [
        (r"Добавить книгу ([\d\-\.A-Яа-яA-Za-z\s]+)", library.append),
        (r"Удалить книгу ([\d\-\.A-Яа-яA-Za-z\s]+)", library.remove),
        (
            r"Найти книгу по автору - ([\d\-\.A-Яа-яA-Za-z\s]+)",
            partial(library.search_books, "author"),
        ),
        (
            r"Найти книгу по названию - ([\d\-\.A-Яа-яA-Za-z\s]+)",
            partial(library.search_books, "title"),
        ),
        (r"Найти книгу по году - (\d+)", partial(library.search_books, "year")),
        (
            r"Отсортировать книги по годам",
            partial(Library.sort_books, key=lambda book: book.year),
        ),
        (
            r"Отсортировать книги по авторам",
            partial(Library.sort_books, key=lambda book: book.author),
        ),
        (
            r"Отсортировать книги по названиям",
            partial(Library.sort_books, key=lambda book: book.title),
        ),
    ]

    for pattern, method in patterns:
        if res := re.fullmatch(pattern, what_to_do.strip(), re.I):
            if re.match("Отсортировать", what_to_do.strip(), re.I):
                return method(library)

            result = method(res.group(1))

            return result if result is not None else library.to_pretty_table()

    return "Не выполнено"


def fifth_question(what_to_do: str):
    """
    Класс Покупатель: Фамилия, Имя, Отчество, Адрес, Номер кредитной карточки, Номер банковского счета;
    Методы: установка значений атрибутов, получение значений атрибутов, вывод информации.
    Создать массив объектов данного класса. Вывести список покупателей в алфавитном порядке и список покупателей,
    у которых номер кредитной карточки находится в заданном диапазоне.
    Пример ввода:
    Вывести список покупателей, у которых номер кредитной карточки находится в диапазоне от 100 до 10000000
    """

    buyers = [generate_buyer() for _ in range(10)]

    if re.fullmatch(
        r"Вывести список покупателей в алфавитном порядке", what_to_do.strip()
    ):
        buyers.sort(key=lambda x: x.full_name)
        return "\n\n".join(map(str, buyers))

    pattern = r"Вывести список покупателей, у которых номер кредитной карточки находится в диапазоне от (\d+) до (\d+)"
    if res := re.fullmatch(pattern, what_to_do.strip()):
        min_num, max_num = map(int, res.groups())
        return "\n\n".join(
            map(
                str,
                filter(
                    lambda buyer: min_num <= buyer.credit_card_number <= max_num, buyers
                ),
            )
        )


def sixth_question(what_to_do: str):
    """
    Класс Абонент: Идентификационный номер, Фамилия, Имя, Отчество, Адрес, Номер кредитной карточки, Дебет, Кредит,
    Время междугородных и городских переговоров; Конструктор;
    Методы: установка значений атрибутов, получение значений атрибутов, вывод информации.
    Создать массив объектов данного класса.
    Вывести сведения относительно абонентов, у которых время городских переговоров превышает заданное.
    Сведения относительно абонентов, которые пользовались междугородной связью.
    Список абонентов в алфавитном порядке.
    """
    subscribers = [generate_subscriber() for _ in range(10)]

    patterns = [
        (
            r"Вывести сведения относительно абонентов, у которых время превышает (\d{2}:\d{2}:\d{2})",
            lambda x, mat: x.local_call_time > arrow.get(mat.group(1)).time(),
        ),
        (
            r"Вывести сведения относительно абонентов, которые пользовались междугородной связью",
            lambda x, _: x.intercity_call_time
            > arrow.get("00:01:00", "HH:mm:ss").time(),
        ),
        (r"Вывести список абонентов в алфавитном порядке", None),
    ]

    for pattern, condition in patterns:
        if match := re.fullmatch(pattern, what_to_do.strip()):
            if condition is None:
                iterable = sorted(subscribers, key=lambda x: x.full_name)
            else:
                iterable = filter(lambda x: condition(x, match), subscribers)

            return "\n\n".join(map(str, iterable))

    return "Неверный формат ввода"


def seventh_question(what_to_do: str):
    """
    Построить три класса (базовый и 3 потомка), описывающих некоторых хищных животных (один из потомков),
    всеядных(второй потомок) и травоядных (третий потомок).
    Описать в базовом классе абстрактный метод для расчета количества и типа пищи,
    необходимого для пропитания животного в зоопарке.
    a) Упорядочить всю последовательность животных по убыванию количества пищи.
    При совпадении значений – упорядочивать данные по алфавиту по имени.
    Вывести идентификатор животного, имя, тип и количество потребляемой пищи для всех элементов списка.
    b) Вывести первые 5 имен животных из полученного в пункте а) списка.
    c) Вывести последние 3 идентификатора животных из полученного в пункте а) списка.
    d) Организовать запись и чтение коллекции в/из файла.
    e) Организовать обработку некорректного формата входного файла.
    """

    animals = [generate_animal(i) for i in range(10)]

    patterns_and_functions = [
        (
            r"Упорядочить всю последовательность животных по убыванию количества пищи.",
            lambda: sorted(map(lambda x: x.food_requirements(), animals)),
        ),
        (
            r"Вывести первые 5 имен животных из полученного в пункте а\) списка.",
            lambda: sorted(map(lambda x: x.food_requirements(), animals))[:5],
        ),
        (
            r"Вывести последние 3 идентификатора животных из полученного в пункте а\) списка.",
            lambda: sorted(map(lambda x: x.food_requirements(), animals))[-3:],
        ),
        (r"Прочитать json файл", read_from_file),
        (
            r"Записать в json файл",
            partial(write_to_file, list(map(lambda x: x.food_requirements(), animals))),
        ),
    ]

    for pattern, function in patterns_and_functions:
        if re.fullmatch(pattern, what_to_do.strip(), re.IGNORECASE | re.MULTILINE):
            return function() if function is not None else "Выполнено!"

    return "Ввели неверное задание"


def main() -> None:
    match input("Выберите номер задания: "):
        case "1":
            pprint(first_question(input("Введите что вы хотите сделать: ")))
        case "2":
            print(second_question(input("Введите что вы хотите сделать: ")))
        case "3":
            print(third_question(input("Введите что вы хотите сделать: ")))
        case "4":
            pprint(fourth_question(input("Введите что вы хотите сделать: ")))
        case "5":
            print(fifth_question(input("Введите что вы хотите сделать: ")))
        case "6":
            print(sixth_question(input("Введите что вы хотите сделать: ")))
        case "7":
            pprint(seventh_question(input("Введите что вы хотите сделать: ")))
        case _:
            print("Вы выбрали неверное задание ")


if __name__ == "__main__":
    main()
