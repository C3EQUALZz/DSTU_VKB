"""
Вариант 4. Написать и протестировать функцию, преобразующую строку восьмеричных
цифр в эквивалентное ей целое десятичное число.
"""

def octal_to_decimal(octal_str: str) -> int:
    """
    Преобразует строку восьмеричных цифр в целое десятичное число.

    Args:
        octal_str: Строка, содержащая восьмеричное число (может иметь префикс '0o' или не иметь)

    Returns:
        Целое десятичное число

    Raises:
        ValueError: Если строка содержит недопустимые символы
    """
    # Удаляем префикс '0o' или '0O', если он присутствует
    if octal_str.startswith('0o') or octal_str.startswith('0O'):
        octal_str = octal_str[2:]

    # Проверка на пустую строку
    if not octal_str:
        return 0

    # Проверяем, что все символы - восьмеричные цифры
    if not all(char in '01234567' for char in octal_str):
        raise ValueError("Строка содержит недопустимые символы для восьмеричного числа")

    # Преобразуем восьмеричную строку в десятичное число
    decimal: int = 0
    for digit in octal_str:
        decimal: int = decimal * 8 + int(digit)
    return decimal