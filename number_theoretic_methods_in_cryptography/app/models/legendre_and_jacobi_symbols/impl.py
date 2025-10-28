from copy import copy
from typing import Final, Iterable, override

from app.core.registry import LogRegistry
from app.models.legendre_and_jacobi_symbols.base import ILegendreJacobiModel


class LegendreJacobiModel(ILegendreJacobiModel):
    """
    Модель для вычисления символов Лежандра и Якоби.

    Символы Лежандра и Якоби используются в теории чисел для определения того,
    является ли число квадратичным вычетом по заданному модулю.

    ОСНОВНЫЕ ПОНЯТИЯ:
    - Квадратичный вычет: число a называется квадратичным вычетом по модулю n,
      если существует такое x, что x² ≡ a (mod n)
    - Неквадратичный вычет: число a называется неквадратичным вычетом по модулю n,
      если не существует такого x, что x² ≡ a (mod n)

    ПРИМЕНЕНИЕ:
    - Символ Лежандра: используется для простых модулей
    - Символ Якоби: обобщение символа Лежандра для составных модулей
    - Применяются в криптографии, алгоритмах факторизации, проверке простоты

    АЛГОРИТМЫ:
    - Символ Лежандра: формула Эйлера a^((p-1)/2) mod p
    - Символ Якоби: рекурсивный алгоритм на основе квадратичного закона взаимности
    """
    
    def __init__(self) -> None:
        self._legendre_registry: Final[LogRegistry] = LogRegistry()
        self._jacobi_registry: Final[LogRegistry] = LogRegistry()

    @override
    def calculate_legendre(self, numerator: int, prime_denominator: int) -> int:
        """
        Вычисляет символ Лежандра (a|p) для целого числа a и простого числа p.

        Символ Лежандра определяется как:
            - 0, если a ≡ 0 mod p (a делится на p)
            - 1, если a — квадратичный вычет по модулю p (существует x: x² ≡ a mod p)
            - -1, если a — неквадратичный вычет по модулю p (не существует такого x)

        АЛГОРИТМ (формула Эйлера):
        1. Проверяем, что p — простое число
        2. Если a ≡ 0 mod p, возвращаем 0
        3. Если a ≡ 1 mod p, возвращаем 1
        4. Иначе вычисляем: (a|p) ≡ a^((p-1)/2) mod p
        5. Если результат = 1, то a — квадратичный вычет (возвращаем 1)
        6. Если результат = p-1, то a — неквадратичный вычет (возвращаем -1)

        МАТЕМАТИЧЕСКОЕ ОБОСНОВАНИЕ:
        По малой теореме Ферма: a^(p-1) ≡ 1 mod p для простого p и НОД(a,p) = 1
        Отсюда: a^(p-1) - 1 = (a^((p-1)/2) - 1)(a^((p-1)/2) + 1) ≡ 0 mod p
        Значит: a^((p-1)/2) ≡ ±1 mod p
        Если a^((p-1)/2) ≡ 1 mod p, то a — квадратичный вычет
        Если a^((p-1)/2) ≡ -1 mod p, то a — неквадратичный вычет

        Args:
            numerator: Числитель символа Лежандра (a)
            prime_denominator: Простое число — знаменатель символа Лежандра (p)

        Returns:
            int: Символ Лежандра (a|p), принимающий значения:
                - 1: a — квадратичный вычет по модулю p
                - -1: a — неквадратичный вычет по модулю p  
                - 0: a делится на p
                - -2: ошибка (p не простое число)
        """
        self._legendre_registry.add_log(
            f"Вычисление символа Лежандра для ({numerator}/{prime_denominator})"
        )

        if prime_denominator <= 1 or not self.__is_prime(prime_denominator):
            error_msg = "Знаменатель должен быть простым числом"
            self._legendre_registry.add_log(f"Ошибка: {error_msg}")
            return -2

        if numerator == 0 or numerator == 1:
            self._legendre_registry.add_log(
                f"Числитель равен {numerator}, возвращаем результат: {numerator}"
            )
            return numerator

        current_numerator: int = numerator % prime_denominator
        self._legendre_registry.add_log(
            f"Приводим числитель к модулю простого знаменателя: {current_numerator}"
        )

        exponent = (prime_denominator - 1) // 2
        self._legendre_registry.add_log(
            f"Вычисляем показатель степени e = (p-1)//2 = {exponent}"
        )

        result: int = pow(current_numerator, exponent, prime_denominator)
        self._legendre_registry.add_log(
            f"Вычисляем pow({current_numerator}, {exponent}, {prime_denominator}) = {result}"
        )

        if result == 1:
            self._legendre_registry.add_log("Результат = 1 (квадратичный вычет)")
            return 1
        elif result == prime_denominator - 1:
            self._legendre_registry.add_log("Результат = -1 (неквадратичный вычет)")
            return -1

        self._legendre_registry.add_log("Результат = 0 (числитель делится на знаменатель)")
        return 0

    @override
    def calculate_jacobi(self, numerator: int, denominator: int) -> int:
        """
        Вычисляет символ Якоби (a/n) для целого числа a и нечетного положительного числа n.

        Символ Якоби — это обобщение символа Лежандра на случай составных знаменателей.
        Если n = p1^e1 * p2^e2 * ... * pk^ek, то:
        (a/n) = (a/p1)^e1 * (a/p2)^e2 * ... * (a/pk)^ek

        Символ Якоби принимает значения:
            - 0, если НОД(a, n) ≠ 1 (a и n не взаимно просты)
            - 1, если НОД(a, n) = 1 и a — квадратичный вычет по модулю n
            - -1, если НОД(a, n) = 1 и a — неквадратичный вычет по модулю n

        АЛГОРИТМ (основан на квадратичном законе взаимности):
        1. Приводим a по модулю n: a = a mod n
        2. Если a = 0, возвращаем 0
        3. Инициализируем знак результата = 1
        4. Пока a ≠ 0:
           a) Удаляем все множители 2 из a:
              - Для каждого удаленного множителя 2:
                если n ≡ 3 или 5 (mod 8), то меняем знак результата
           b) Меняем местами a и n (квадратичный закон взаимности)
           c) Если a ≡ n ≡ 3 (mod 4), то меняем знак результата
           d) Приводим a по модулю n: a = a mod n
        5. Если n = 1, возвращаем знак результата
        6. Иначе возвращаем 0

        МАТЕМАТИЧЕСКИЕ СВОЙСТВА:
        - Квадратичный закон взаимности: если p, q — различные нечетные простые числа,
          то (p/q) * (q/p) = (-1)^((p-1)/2 * (q-1)/2)
        - Правило для множителя 2: (2/p) = (-1)^((p²-1)/8)
        - Мультипликативность: (ab/n) = (a/n) * (b/n)

        Args:
            numerator: Числитель символа Якоби (a)
            denominator: Знаменатель символа Якоби (n), должен быть положительным нечетным числом

        Returns:
            int: Символ Якоби (a/n), принимающий значения -1, 0 или 1

        Raises:
            ValueError: Если знаменатель не положителен или четен
        """
        self._jacobi_registry.add_log(f"Вычисление символа Якоби для ({numerator}/{denominator})")

        if denominator <= 0 or denominator % 2 == 0:
            raise ValueError("Знаменатель должен быть положительным нечетным числом")

        # Приведение числителя по модулю знаменателя
        current_numerator: int = numerator % denominator
        self._jacobi_registry.add_log(f"Приводим числитель к модулю знаменателя: a = {current_numerator}")

        if current_numerator == 0:
            self._jacobi_registry.add_log("Числитель = 0 mod знаменатель, результат: 0")
            return 0

        # Переменная для хранения знака результата
        result_sign: int = 1

        while current_numerator != 0:
            # Шаг 1: Удаление всех множителей 2 из числителя
            while current_numerator % 2 == 0:
                current_numerator //= 2
                mod8_remainder = denominator % 8

                if mod8_remainder in (3, 5):
                    result_sign *= -1

                self._jacobi_registry.add_log(
                    f"Числитель четное, делим на 2 -> a={current_numerator}, sign={result_sign}")

            # Шаг 2: Обмен числителя и знаменателя
            current_numerator, denominator = denominator, current_numerator
            self._jacobi_registry.add_log(
                f"Меняем местами числитель и знаменатель: a={current_numerator}, n={denominator}")

            # Шаг 3: Изменение знака при условии a ≡ n ≡ 3 mod 4
            if current_numerator % 4 == 3 and denominator % 4 == 3:
                result_sign *= -1
                self._jacobi_registry.add_log(f"a = 3 mod 4 и n = 3 mod 4 → изменение знака sign={result_sign}")

            # Шаг 4: Приведение числителя по модулю знаменателя
            current_numerator = current_numerator % denominator
            self._jacobi_registry.add_log(f"Приводим числитель к модулю знаменателя: a={current_numerator}")

        # Шаг 5: Проверка завершения алгоритма
        if denominator == 1:
            self._jacobi_registry.add_log(f"Знаменатель = 1, возвращаем результат: {result_sign}")
            return result_sign
        else:
            self._jacobi_registry.add_log(f"Знаменатель != 1, возвращаем результат: 0")
            return 0

    @staticmethod
    def __is_prime(n: int) -> bool:
        """
        Проверяет, является ли число простым.

        АЛГОРИТМ (проверка делителей):
        1. Если n < 2, то n не простое
        2. Проверяем все возможные делители от 2 до √n
        3. Если найден делитель, то n составное
        4. Если делителей нет, то n простое

        МАТЕМАТИЧЕСКОЕ ОБОСНОВАНИЕ:
        Если n составное, то n = a * b, где 1 < a ≤ b < n
        Тогда a ≤ √n, поэтому достаточно проверить делители до √n

        Args:
            n: Число для проверки

        Returns:
            bool: True, если n простое, False иначе

        """
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    @override
    def get_legendre_logs(self) -> Iterable[str]:
        result: Iterable[str] = copy(self._legendre_registry.logs)
        self._legendre_registry.clear_logs()
        return result

    @override
    def get_jacobi_logs(self) -> Iterable[str]:
        result: Iterable[str] = copy(self._jacobi_registry.logs)
        self._jacobi_registry.clear_logs()
        return result