"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""
import re

########################################################################################################################
import numpy as np
from mimesis import Person, Address, Datetime
from mimesis.locales import Locale
from prettytable import PrettyTable

########################################################################################################################
from python_language.programming_languages_python.fourteenth_laba_lang.classes import (Student,
                                                                                       Train,
                                                                                       Trains,
                                                                                       TwoVariables)
from python_language.programming_languages_python.fourteenth_laba_lang.help_functions import generate_table


def first_question(k=None) -> PrettyTable:
    """
    Создать класс Student, содержащий поля: фамилия и инициалы, номер группы, успеваемость (массив из пяти элементов).
    Создать массив из десяти элементов такого типа, упорядочить записи по возрастанию среднего балла.
    Добавить возможность вывода фамилий и номеров групп студентов, имеющих оценки, равные только 4 или 5.
    """
    # mimesis не поддерживает отчества, так как в английском их нет, поэтому такая затычка будет.
    students: np.ndarray[Student, ...] = np.array([
        Student(
            last_name=person.surname(),
            initials=f"{person.name()[0]}.{person.name()[-1].upper()}",
            number_group=np.random.randint(1, 10),
            grades=np.random.uniform(2.0, 5.0, 5).round(2)
        )

        for _ in range(10)
        if (person := Person(Locale.RU))
    ])

    return generate_table(students)


def second_question(what_to_do: str) -> str | PrettyTable:
    """
    Создать класс с именем Train, содержащий поля: название пункта назначения, номер поезда, время отправления.
    Ввести данные в массив из пяти элементов типа train, упорядочить элементы по номерам поездов.
    Добавить возможность вывода информации о поезде, номер которого введен пользователем.
    Добавить возможность сортировки массива по пункту назначения, причем поезда с одинаковыми пунктами назначения
    должны быть упорядочены по времени отправления.
    """
    list_trains = np.array([
        Train(
            dest=f"{destination.federal_subject()} г.{destination.city()}",
            number=number,
            departure=Datetime().time().replace(microsecond=0)
        )

        for number in range(1, 6)
        if (destination := Address(Locale.RU))
    ])

    trains = Trains(trains=list_trains)

    if reg := re.fullmatch(r"^Вывести информацию о поезде под номером (\d+)$", what_to_do.strip(), re.I):
        return trains[trains.find(int(reg.group(1)))].info

    elif re.fullmatch(r"^Отсортировать поезда по пункту назначения|Отсортировать$", what_to_do.strip(), re.I):
        trains.sort(lambda train: (train.dest, train.departure))
        return generate_table(trains.trains)

    elif re.fullmatch(r"^Вывести всю таблицу расписания поездов$", what_to_do.strip(), re.I):
        return generate_table(trains.trains)

    return "Вы неправильно ввели"


def third_question(string: str):
    """
    Создать класс с двумя переменными.
    Добавить функцию вывода на экран и функцию изменения этих переменных.
    Добавить функцию, которая находит сумму значений этих переменных.
    Функцию, которая находит наибольшее значение из этих двух переменных.
    """
    if res := re.fullmatch(r"^Найти сумму значений (?:переменных)?(\d+) (\d+)$", string.strip(), re.I):
        var = TwoVariables(*map(int, res.groups()))
        return var.sum()

    if res := re.fullmatch(r"^Найти наибольшее значение (\d+) (\d+)$", string.strip(), re.I):
        var = TwoVariables(*map(int, res.groups()))
        return var.max_variable()

    if res := re.fullmatch(r"^Изменить переменные с (\d+ \d+) на (\d+ \d+)$", string.strip(), re.I):
        var = TwoVariables(*map(int, res.group(1).split()))
        return var.modify(*map(int, res.group(2).split()))


def fourth_question(k=None):
    """
    Класс «Домашняя библиотека». Предусмотреть возможность работы с произвольным числом книг, поиска книги по
    какому-либо признаку (например, по автору или по году издания), добавления книг в библиотеку,
    удаления книг из нее, сортировки книг по разным полям.
    """
    ...


def fifth_question(k=None):
    """
    Класс Покупатель: Фамилия, Имя, Отчество, Адрес, Номер кредитной карточки, Номер банковского счета;
    Методы: установка значений атрибутов, получение значений атрибутов, вывод информации.
    Создать массив объектов данного класса. Вывести список покупателей в алфавитном порядке и список покупателей,
    у которых номер кредитной карточки находится в заданном диапазоне.
    """
    ...


def sixth_question(k=None):
    """
    Класс Абонент: Идентификационный номер, Фамилия, Имя, Отчество, Адрес, Номер кредитной карточки, Дебет, Кредит,
    Время междугородных и городских переговоров; Конструктор;
    Методы: установка значений атрибутов, получение значений атрибутов, вывод информации.
    Создать массив объектов данного класса.
    Вывести сведения относительно абонентов, у которых время городских переговоров превышает заданное.
    Сведения относительно абонентов, которые пользовались междугородной связью.
    Список абонентов в алфавитном порядке.
    """
    ...


def seventh_question(k=None):
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
    ...


def main() -> None:
    match input("Выберите номер задания: "):
        case "1":
            print(first_question())
        case "2":
            print(second_question(input("Введите что вы хотите сделать: ")))
        case "3":
            print(third_question(input("Введите что вы хотите сделать: ")))
        case "4":
            print(fourth_question())
        case "5":
            print(fifth_question())
        case "6":
            print(sixth_question())
        case "7":
            print(seventh_question())
        case _:
            print("Вы выбрали неверное задание ")


if __name__ == "__main__":
    main()
