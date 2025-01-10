"""
Задача №774. Шифровка

Шпион Коля зашифровал и послал в центр радиограмму.
Он использовал такой способ шифровки: сначала выписал все символы своего сообщения (включая знаки препинания и т.п.),
стоявшие на четных местах, в том же порядке, а затем – все символы, стоящие на нечетных местах.
Напишите программу, которая расшифровывает сообщение.

Входные данные

Вводится одна непустая строка длиной не более 250 символов – зашифрованное сообщение.
Строка может состоять из любых символов, кроме пробельных.

Выходные данные

Выведите одну строку – расшифрованное сообщение.
"""
from typing import List, AnyStr


def decrypt_message(encrypted_message: AnyStr) -> AnyStr:
    """
    :param encrypted_message: сообщение, которое мы хотим расшифровать по условию задания.
    :returns:
    Args:
        encrypted_message:

    Returns:

    """
    symbols: List[AnyStr] = list(encrypted_message)
    n: int = len(encrypted_message) // 2
    for i in range(n):
        symbols[2 * i: 2 * i + 2] = encrypted_message[i + n], encrypted_message[i]

    return ''.join(symbols)


def main() -> None:
    # Чтение входных данных
    encrypted_message = input()

    # Получение расшифрованного сообщения
    decrypted_message: str = decrypt_message(encrypted_message)

    # Вывод результата
    print(decrypted_message)


if __name__ == '__main__':
    main()
