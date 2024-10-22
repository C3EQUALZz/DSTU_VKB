"""
Напишите функцию, которая будет производить поиск по значению и выдавать ключ.
"""
import ast


def search_key(value: str, dictionary: dict[str, str]) -> str:
    for k, v in dictionary.items():
        if str(v) == value:
            return k

    return "Нет ключа соотв. данному значению в словаре"


def main() -> None:
    user_input = input("Вводите словарь по следующему правилу {key: value, key: value, ...}: ")
    dictionary: dict[str, str] = ast.literal_eval(user_input)
    print(dictionary)
    value = input("Введите значение ")
    print(search_key(value, dictionary))


if __name__ == '__main__':
    main()
