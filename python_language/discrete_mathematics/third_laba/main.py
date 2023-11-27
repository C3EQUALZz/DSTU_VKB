"""
Главный файл, где происходит стартовая точка.
Здесь описана логика алгоритма: https://klanec.github.io/rgbctf/2020/07/22/rgbctf-RubiksCBC.html
Скорее всего, операция шифрования - это просто перестановка кубика Рубика каждого блока.

Логика здесь:
    -
"""
from python_language.discrete_mathematics.third_laba.background_logic.encryption_text_logic import byte_encryption_text


def terminal_main():
    data = input("Введите ваше сообщение, которое хотите зашифровать ")
    print(byte_encryption_text(data))
