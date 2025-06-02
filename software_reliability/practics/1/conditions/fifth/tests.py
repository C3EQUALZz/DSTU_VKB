import pytest

from conditions.fifth.main import calculate_u  # Замените your_module на имя вашего модуля


def test_positive_condition():
    """Тест случая, когда сумма произведений > 0"""
    x = [1.0] * 20
    y = [1.0] * 20
    # Сумма произведений (15*1=15) > 0 -> u = сумма квадратов всех x
    assert calculate_u(x, y) == 20.0


def test_negative_condition():
    """Тест случая, когда сумма произведений <= 0"""
    x = [1.0] * 20
    y = [-1.0] * 20
    # Сумма произведений (15*(-1)=-15) <= 0 -> u = сумма квадратов y[9:19]
    assert calculate_u(x, y) == 10.0


def test_zero_condition():
    """Тест случая, когда сумма произведений = 0"""
    x = [0.0] * 20
    y = [0.0] * 20
    # Сумма произведений = 0 -> u = сумма квадратов y[9:19]
    assert calculate_u(x, y) == 0.0


def test_mixed_values():
    """Тест со смешанными значениями"""
    x = [i for i in range(20)]  # [0,1,2,...,19]
    y = [-i for i in range(20)]  # [0,-1,-2,...,-19]

    # Сумма произведений = sum(i*(-i) for i in range(15))
    # = -sum(i^2) for i=0..14 = - (14*15*29)//6 = -1015 < 0
    # u = сумма y[9]^2 до y[18]^2 = sum(i^2) for i=9..18
    expected = sum(i ** 2 for i in range(9, 19))
    assert calculate_u(x, y) == expected


def test_float_values():
    """Тест с вещественными числами"""
    x = [0.5] * 20
    y = [2.0] * 20
    # Сумма произведений (15*0.5*2=15) > 0 -> u = сумма квадратов всех x
    assert calculate_u(x, y) == 20 * (0.5 ** 2)


def test_invalid_input():
    """Тест обработки неверного размера массивов"""
    with pytest.raises(ValueError):
        calculate_u([1] * 19, [1] * 20)  # Неправильный размер X

    with pytest.raises(ValueError):
        calculate_u([1] * 20, [1] * 19)  # Неправильный размер Y

    with pytest.raises(ValueError):
        calculate_u([1] * 25, [1] * 25)  # Оба массива неверного размера


def test_edge_case():
    """Тест пограничного случая (сумма произведений = 0)"""
    x = [1.0] * 20
    y = [0.0] * 20
    # Сумма произведений = 0 -> u = сумма квадратов y[9:19]
    assert calculate_u(x, y) == 0.0
