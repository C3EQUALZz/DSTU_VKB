"""
Здесь реализация логики возвращения от Полинома Жегалкина к вектору.
P = z ⊕ y ⊕ yz ⊕ xz ⊕ xyz
Правильный вектор функции f должен быть следующим:
f=(0,1,1,1,0,0,1,1)

f(0,0,0)= 0 ⊕ 0 ⊕ 0 * 0 ⊕ 0 * 0 ⊕ 0 * 0 * 0 = 0
f(0,0,1)= 1 ⊕ 0 ⊕ 0 * 1 ⊕ 0 * 1 ⊕ 0 * 0 * 1 = 1 и т.д
f(0,1,0)=1
f(0,1,1)=1
f(1,0,0)=0
f(1,0,1)=0
f(1,1,0)=1
f(1,1,1)=1

"""
import sympy
import itertools
import re


def parse_input(string_polynom: str) -> sympy.Xor:
    """
    Здесь преобразование пользовательского ввода для парсинга библиотекой
    """
    # Тут мы делим на "^" или "xor", удаляем пробелы лишние и соединяем через класс Xor.
    #fixme Не сделал поддержку ввода без звездочки
    return sympy.Xor(*[monom for monom in map(str.strip, re.split(r"\^|\bxor\b", string_polynom))])


def vector_from_polynom(polynomial_str: str):
    """
    Получаем вектор из полинома.
    Здесь использована такая идея: каждую строку таблицы поставляем в значения формулы Жегалкина.
    """
    # Извлечение символов из полинома
    variable_names = sympy.symbols(' '.join(sorted(set(re.findall(r'\b[a-zA-Z]\b', polynomial_str)))))
    parsed_input = parse_input(polynomial_str)
    # Создаем таблицу истинности и проходимся построчно. Здесь subs подставляет значение каждой строки
    # в наш полином Жегалкина, он может вернуть так int, так особый класс sumpy.logic.BooleanTrue
    list_with_results = [int(bool(parsed_input.subs(dict(zip(variable_names, row))))) for row in
                         itertools.product([0, 1], repeat=len(variable_names))]
    return list_with_results
