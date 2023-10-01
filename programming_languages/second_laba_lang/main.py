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
    print(f"{my_number=}, {user_number=}")


def second_question(my_list: list):
    """
    Пусть задан список, содержащий строки.
    Вариант 1. Выведите построчно все строки размером от 5 до 10 символов.
    """
    print(*filter(lambda x: 5 <= len(str(x)) <= 10, my_list), sep='\n')


def third_question():
    """
    Сгенерируйте и выведите:
    Вариант 1. Случайную строку, состоящую из 5 символов, содержащую
    только заглавные буквы русского алфавита.
    """
    print(''.join(sample(ascii_uppercase, 5)))


def fourth_question(string: str):
    """
    Пусть дана строка:
    Вариант 1. На основе данной строки сформируйте новую, содержащую только цифры. Выведите новую строку.
    """
    print(f"Цифры - {''.join(filter(lambda x: x.isdigit(), string))}")


def main():
    match input("Введите номер задания "):
        case "1":
            first_question(int(input("Введите my_number ")))
        case "2":
            second_question(eval(input("Введите список, как он выглядит в repr ")))
        case "3":
            third_question()
        case "4":
            fourth_question(input("Введите вашу строку, состоящую из цифр и чисел "))
        case _:
            print("Вы выбрали неверный номер ")


if __name__ == "__main__":
    main()
