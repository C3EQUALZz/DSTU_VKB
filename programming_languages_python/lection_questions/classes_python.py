from functools import wraps


class Person:
    name = ""
    money = 0

    def out(self):
        print(self.name, self.money)


class Critter():
    """Виртуальный питомец"""

    def __init__(self):  # метод-конструктор
        print("На лекции")

    def __init__(self):
        print("Привет")

    def talk(self):
        print("\n Привет.  Я животное – экземпляр класса Critter.")


class Critter2:
    """Виртуальный питомец"""

    def __init__(self, name):
        print("Появилось на свет новое животное!")
        self.name = name

    def __str__(self):  # возвращает строку, которая
        rep = "Объект класса Critter\n"  # содержит значение
        rep += "имя: " + self.name + "\n"  # атрибута name
        return rep

    def talk(self):
        print("Привет.  Меня зовут", self.name, "\n")

    def something(self):
        print(self.name + " Мяу!")


class Critter3:
    """Виртуальный питомец"""
    total = 0  # атрибут класса

    @staticmethod  # декоратор меняет смысл метода
    def status():  # статический метод, отсутствует self
        print("\nВсего животных сейчас", Critter3.total)

    def __init__(self, name):
        print("Появилось на свет новое животное!")
        self.name = name
        Critter3.total += 1


def counter(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print("Hello ")
        return func(*args, **kwargs)

    return inner


@counter
def pupa():
    """
    Привет
    """
    print("Kekw")


print(pupa.__doc__)
