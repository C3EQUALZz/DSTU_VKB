import re
from typing import Any

from app.logic.dtos.cyclic_codes import EncodedAndPolynomDTO


class CyclicCodeService:
    @staticmethod
    def encode(symbols_to_encode: str, matrix: list[list[int]]) -> EncodedAndPolynomDTO:
        terms: str = " + ".join(
            f"x^{i}"
            for i, bit in enumerate(symbols_to_encode)
            if bit == "1"
        )

        selected_rows: list[list[int]] = [row for row, bit in zip(matrix, symbols_to_encode) if str(bit) == "1"]

        encoded_str: str = "".join(str(sum(col) % 2) for col in zip(*selected_rows))

        return EncodedAndPolynomDTO(
            terms,
            encoded_str
        )

    @staticmethod
    def pols_to_coefficients(poly_str: str) -> list[int]:
        """Преобразует строку полинома в список коэффициентов (от x⁰ к xⁿ)."""
        coefficients_dict = {}
        terms = re.split(r'\s*[+-]\s*', poly_str.replace(' ', ''))
        for term in terms:
            if not term:
                continue
            sign = 1
            if term.startswith('-'):
                sign = -1
                term = term[1:]
            if term == 'x':
                coeff, power = 1, 1
            elif 'x^' in term:
                coeff_part, power_part = term.split('x^')
                coeff = int(coeff_part) if coeff_part else 1
                power = int(power_part)
            elif 'x' in term:
                coeff_part = term.split('x')[0]
                coeff = int(coeff_part) if coeff_part else 1
                power = 1
            else:
                coeff = int(term)
                power = 0
            coefficients_dict[power] = (sign * coeff) % 2  # GF(2)
        max_power = max(coefficients_dict.keys()) if coefficients_dict else 0
        return [coefficients_dict.get(i, 0) for i in range(max_power + 1)]

    @staticmethod
    def cyclic_shift(vec: list[Any], shifts: int) -> list[Any]:
        """Циклический сдвиг вектора вправо."""
        shifts = shifts % len(vec)
        return vec[-shifts:] + vec[:-shifts]

    @staticmethod
    def divide_polynomials(dividend: list[int], divisor: list[int]) -> tuple[list[int], list[int]]:
        """Деление полиномов в GF(2) с возвратом частного и остатка."""
        dividend = dividend.copy()
        divisor_degree = len(divisor) - 1
        quotient = []

        while len(dividend) >= len(divisor):
            current_degree = len(dividend) - 1
            if current_degree < divisor_degree:
                break

            # Вычисляем множитель
            term = [0] * (current_degree - divisor_degree) + divisor
            term += [0] * (len(dividend) - len(term))

            # XOR операции
            new_dividend = [(a ^ b) for a, b in zip(dividend, term)]

            # Удаляем ведущие нули
            while len(new_dividend) > 0 and new_dividend[0] == 0:
                new_dividend.pop(0)

            quotient.append(1)
            dividend = new_dividend

        # Остаток дополняем ведущими нулями до степени делителя
        remainder = [0] * divisor_degree
        if len(dividend) > 0:
            remainder = [0] * (divisor_degree - len(dividend)) + dividend

        return quotient, remainder

    def decode(self, v: str, g_poly_str: str) -> str:
        # Преобразуем входную строку в список чисел
        v_list = [int(bit) for bit in v]

        # Получаем коэффициенты порождающего полинома
        g_coeffs = self.pols_to_coefficients(g_poly_str)
        n = len(v_list)
        k = n - (len(g_coeffs) - 1)  # Длина информационного слова

        # Вычисляем синдром
        _, remainder = self.divide_polynomials(v_list.copy(), g_coeffs)

        # Циклический перебор ошибок
        for shift in range(n):
            # Проверяем остаток на наличие ошибки в старшем разряде
            if remainder == [1] + [0] * (len(g_coeffs) - 2):
                # Исправляем ошибку
                error_pos = (n - 1 - shift) % n
                v_list[error_pos] ^= 1

                # Пересчитываем синдром после исправления
                _, new_remainder = self.divide_polynomials(v_list, g_coeffs)
                if sum(new_remainder) == 0:
                    return ''.join(map(str, v_list[:k]))

            # Циклический сдвиг остатка
            remainder = self.cyclic_shift(remainder, 1)
            if len(remainder) < len(g_coeffs) - 1:
                remainder = [0] * (len(g_coeffs) - 1 - len(remainder)) + remainder

        raise ValueError("Декодирование не удалось")
