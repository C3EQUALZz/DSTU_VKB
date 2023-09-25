"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""
from prettytable import PrettyTable


def first_question(string: str):
    """
    Пусть дана строка, состоящая из слов, пробелов и знаков препинания.
    На основании этой строки создайте новую, содержащую только слова больше 5 символов.
    Разделитель слов в строке - пробел.
    """
    print(' '.join(filter(lambda x: len(x) > 5, string.split())))


def temporary_info(string: list[str]):
    temporary_storage, index_list = [], -1
    for information in string[3:]:
        if information[0].startswith("_"):
            temporary_storage.append([information[1:]])
            index_list += 1
        else:
            temporary_storage[index_list].append(information)
    for index, data in enumerate(temporary_storage):
        data[0:3] = [' '.join(data[0:3])]
        temporary_storage[index].sort(key=len, reverse=True)
    yield from temporary_storage


def second_question():
    """
    Пусть дана строковая переменная my_string, содержащая информацию о студентах.
    Вариант 1. Вывести информацию в виде таблицы
    """
    my_table = PrettyTable()
    my_string = ("Ф;И;О;Возраст;Категория;_Иванов;Иван;Иванович;23 года;Студент 3 курса;_Петров;Семен;Игоревич;22 "
                 "года;Студент 2 курса").split(";")
    my_string[0:3] = [''.join(my_string[0:3])]

    my_table.field_names = my_string[0], my_string[2], my_string[1]

    my_table.add_rows(temporary_info(my_string))
    print(my_table)


def third_question():
    """
    Пусть дана строковая переменная my_string, содержащая информацию о студентах.
    Вариант 1. Вывести построчно информацию о студентах, чья фамилия - "Петров".
    """
    my_string = ("ФИО;Возраст;Категория;_Иванов Иван Иванович;23 года;Студент 3 курса;_Петров Семен Игоревич;22 "
                 "года;Студент 2 курса;_Акибов Ярослав Наумович;23 года;Студент 3 курса;_Борков Станислав Максимович;"
                 "21 год;Студент 1 курса;_Петров Семен Семенович;21 год;Студент 1 курса;_Романов Станислав Андреевич;"
                 "23 года;Студент 3 курса;_Петров Всеволод Борисович;21 год;Студент 2 курса").split(";")

    print(*map(lambda human: human[0], filter(lambda x: x[0].startswith("Петров"), temporary_info(my_string))),
          sep='\n')


def fourth_question(string: str):
    """
    Пусть дана строка произвольной длины. Выведите информацию о том, сколько в ней символов и слов.
    """
    print(f"Количество слов - {len(string.split())}",
          f"Количество символов - {sum(symbol.isalpha() for symbol in string)}", sep='\n')


def main():
    match input("Введите номер задания "):
        case "1":
            first_question(input("Введите строку, состоящую из слов, пробелов и знаков препинания. "))
        case "2":
            second_question()
        case "3":
            third_question()
        case "4":
            fourth_question(input("Введите произвольную строку "))
        case _:
            print("Вы выбрали неверный номер ")


if __name__ == "__main__":
    main()
