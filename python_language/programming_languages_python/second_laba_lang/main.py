"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""
from random import sample
from string import ascii_uppercase


def first_question(my_number: int):
    """
    Пусть задано некоторое число my_number. Пользователь вводит с
    клавиатуры свое число user_number.
    Вариант 1. Запрашивайте у пользователя вводить число user_number до
    тех пор, пока оно не будет меньше my_number.
    """
    while (user_number := int(input("Вводите user_number "))) > my_number:
        continue
    return f"{my_number=}, {user_number=}"


def second_question(my_list: str):
    """
    Пусть задан список, содержащий строки.
    Вариант 1. Выведите построчно все строки размером от 5 до 10 символов.
    """
    return '\n'.join(str(x) for x in filter(lambda x: 5 <= len(str(x)) <= 10, eval(my_list)))


def third_question(s=None):
    """
    Сгенерируйте и выведите:
    Вариант 1. Случайную строку, состоящую из 5 символов, содержащую
    только заглавные буквы русского алфавита.
    """
    return ''.join(sample(ascii_uppercase, 5))


def fourth_question(string: str):
    """
    Пусть дана строка:
    Вариант 1. На основе данной строки сформируйте новую, содержащую только цифры. Выведите новую строку.
    """
    return f"Цифры - {''.join(filter(lambda x: x.isdigit(), string))}"


def main():
    match input("Введите номер задания "):
        case "1":
            print(first_question(int(input("Введите my_number "))))
        case "2":
            print(second_question(input("Введите список, как он выглядит в repr ")))
        case "3":
            print(third_question())
        case "4":
            print(fourth_question(input("Введите вашу строку, состоящую из цифр и чисел ")))
        case _:
            print("Вы выбрали неверный номер ")


if __name__ == "__main__":
    main()
