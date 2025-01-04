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
from typing import List


def decrypt_message(encrypted_message: str) -> str:
    symbols: List[str] = list(encrypted_message)
    n = len(encrypted_message) // 2
    for i in range(n):
        symbols[2 * i: 2 * i + 2] = encrypted_message[i + n], encrypted_message[i]

    return ''.join(symbols)


def main() -> None:
    # Чтение входных данных
    encrypted_message = input()

    # Получение расшифрованного сообщения
    decrypted_message = decrypt_message(encrypted_message)

    # Вывод результата
    print(decrypted_message)


if __name__ == '__main__':
    main()
