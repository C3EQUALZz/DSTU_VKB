"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""
from pprint import pprint

import re
import csv


def read_file(path: str = None) -> list:
    if path.isspace():
        path = "students.csv"
    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        reader.__next__()
        return list(reader)


def first_question(k="students.csv") -> dict:
    """
    Пусть список студентов представлен в виде структуры [[№, ФИО, Возраст, Группа]...].
    Преобразовать список в словарь вида: {№:[ФИО, Возраст, Группа], ....}
    """
    return {person[0]: person[1:] for person in read_file(k)}


class SecondQuestion:
    def __init__(self, input_str: str, data: dict = None):
        self.data = data if data is not None else first_question()
        self.input_str = input_str

    def choice_question(self):
        patterns_and_methods = {
            r"[иИ]зменить возраст \w+\s\w+ на \d+": self.change_age,
            r"[иИ]зменить ФИО студента с \w+\s\w+ на \w+\s\w+": self.change_name,
            r"[уУ]величить возраст студента под номером №\d+ на \d+": self.increase_age_by_number,
            r"[Ии]зменить группу студента \b[A-Za-z]+\s[A-Za-z]+\b на [a-zA-Zа-яА-ЯёЁ]+ - \d+": self.change_group,
            r"[Уу]далить запись о студенте под номером №\d+": self.delete_group
        }

        for pattern, method in patterns_and_methods.items():
            if re.fullmatch(pattern, self.input_str):
                return method(self.input_str)

        # Обработка случая, когда не совпал ни один паттерн
        return None

    @staticmethod
    def extract_info(s: str):
        """
        Вспомогательный метод для нахождения имени человека, возраста, на кого заменить
        """
        person = re.search(r'\b[A-Za-z]+\s[A-Za-z]+\b', s).group(0)
        number_age = int(re.search(r'\d+', s).group(0))
        to_whom_to_change = re.search(r'\b[A-Za-z]+\s[A-Za-z]+\b', s)

        return person, number_age, to_whom_to_change

    def change_age(self, s: str) -> dict:
        """
        Увеличить возраст конкретного студента на какое-то число.
        Пример ввода: Изменить возраст Dwain Huff на 3
        """
        person, number_age, _ = self.extract_info(s)
        for key, value in self.data.items():
            if value[0] == person:
                value[1] = int(value[1]) + number_age
                return {key: value}

    def change_name(self, s: str) -> dict:
        """
        Изменить ФИО студента.
        Пример ввода: изменить ФИО студента с Dwain Huff на Pavel Slesarenko
        """
        who_to_change, to_whom_to_change, _ = self.extract_info(s)
        for key, value in self.data.items():
            if value[0] == who_to_change:
                value[0] = to_whom_to_change
                return {key: value}

    def increase_age_by_number(self, s: str) -> dict:
        number_person, number_age, _ = self.extract_info(s)
        for key, value in self.data.items():
            if key == number_person:
                value[1] = int(value[1]) + abs(number_age)
                return {key: value}

    def change_group(self, s: str) -> dict:
        person, _, new_group = self.extract_info(s)
        for key, value in self.data.items():
            if value[0] == person:
                value[-1] = new_group
                return {key: value}

    def delete_group(self, s: str) -> dict | str:
        try:
            if self.data.pop(re.search(r"\d+", s)):
                return self.data
        except KeyError:
            return "Нет такого ключа"


def second_question(string=None):
    if not re.fullmatch(r"[иИ]зменить возраст \w+\s\w+ на \d+", string):
        return "Неправильно ввели"
    person = re.search(r'\b[A-Za-z]+\s[A-Za-z]+\b', string).group(0)
    number_age = int(re.search(r'\d+', string).group(0))

    for key, value in first_question().items():
        if value[0] == person:
            value[1] = int(value[1]) + number_age
            return {key: value}


def third_question(k=None):
    """
    Добавить возможность вывода из словаря вывод списка студентов группы БО - 111111
    """
    data = first_question()
    return {x: data[x] for x in data if data[x][-1] == "БО - 111111"}


def main() -> None:
    match input("Выберите номер задания "):
        case "1":
            pprint(first_question("students.csv"))
        case "2":
            print("Все студенты, у которых можно увеличить возраст представлены ниже ")
            pprint(data := first_question())
            pprint(
                SecondQuestion(input("Введите что вы хотите сделать, как сказано в условии "), data).choice_question())
        case "3":
            pprint(third_question())


if __name__ == "__main__":
    main()
