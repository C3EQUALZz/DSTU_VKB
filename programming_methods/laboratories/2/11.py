"""
Задача №3722. Корень кубического уравнения

Дано кубическое уравнение ax3+bx2+cx+d=0(a≠0). Известно, что у этого уравнения ровно один корень. Требуется его найти.

Входные данные

Во входных данных через пробел записаны четыре целых числа: −1000≤a,b,c,d≤1000.

Выходные данные

Выведите единственный корень уравнения с точностью не менее 4 знаков после десятичной точки.
"""




def evaluate_polynomial(a: int, b: int, c: int, d: int, x: float) -> float:
    """Вычисляет значение кубического уравнения ax^3 + bx^2 + cx + d."""
    return a * x ** 3 + b * x ** 2 + c * x + d


def evaluate_derivative(a: int, b: int, c: int, x: float) -> float:
    """Вычисляет значение производной кубического уравнения 3ax^2 + 2bx + c."""
    return 3 * a * x ** 2 + 2 * b * x + c


def find_root(a: int, b: int, c: int, d: int, initial_guess: float = 0.0, tolerance: float = 1e-5) -> float:
    """Находит корень кубического уравнения методом Ньютона."""
    x0 = initial_guess

    while True:
        fx = evaluate_polynomial(a, b, c, d, x0)
        f_prime_x = evaluate_derivative(a, b, c, x0)

        # Новое приближение корня
        x1 = x0 - fx / f_prime_x

        # Если разница между приближениями достаточно мала, завершаем итерацию
        if abs(x1 - x0) < tolerance:
            return x1  # Возвращаем найденный корень

        # Обновляем приближение
        x0 = x1
#
#
# def main() -> None:
#     # Читаем коэффициенты кубического уравнения
#     a, b, c, d = map(int, input().split())
#
#     # Находим корень и выводим его с точностью 10 знаков после запятой
#     root = find_root(a, b, c, d)
#     print(root)
#
#
# if __name__ == "__main__":
#     main()

def f(x, a, b, c, d):
    return a * x ** 3 + b * x ** 2 + c * x + d


def bisection(a, b, c, d, left, right, tol=1e-5):
    if f(left, a, b, c, d) * f(right, a, b, c, d) >= 0:
        return find_root(a, b, c, d)

    while (right - left) / 2 > tol:
        midpoint = (left + right) / 2
        if f(midpoint, a, b, c, d) == 0:
            return midpoint  # Найден точный корень
        elif f(left, a, b, c, d) * f(midpoint, a, b, c, d) < 0:
            right = midpoint
        else:
            left = midpoint

    return (left + right) / 2  # Возвращаем приближенный корень


# Пример использования
a, b, c, d = map(int, input().split())

# Ищем корень в интервале [-1000, 1000]
root = bisection(a, b, c, d, -1000, 1000)
print(root)
