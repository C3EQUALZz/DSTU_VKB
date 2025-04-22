import re
from typing import List, Sequence, Tuple, Any

import numpy as np

from app.logic.dtos.cyclic_codes import EncodedAndPolynomDTO


def gf2_polynomial_division(
        dividend: Sequence[int],
        divisor: Sequence[int]
) -> Tuple[List[int], List[int]]:
    """
    Делит полином dividend на divisor в поле GF(2).

    Параметры
    ----------
    dividend : Sequence[int]
        Список бит полинома от старшей степени к младшей (len = n).
    divisor : Sequence[int]
        Список бит порождающего полинома от старшей степени к младшей (len = m+1).

    Возвращает
    -------
    quotient : List[int]
        Коэффициенты частного (len = n-m+1).
    remainder : List[int]
        Остаток степени < m (len = m).
    """
    a = list(dividend)
    n, m = len(a), len(divisor)
    if n < m:
        return [0], a.copy()

    quotient = [0] * (n - m + 1)
    for i in range(n - m + 1):
        if a[i]:
            quotient[i] = 1
            # вычитание в GF(2) = XOR
            for j in range(m):
                a[i + j] ^= divisor[j]
    # остаток — последние m бит
    remainder = a[-m:] if m > 0 else []
    return quotient, remainder


def gf2_solve_linear_system(
        matrix: List[List[int]],
        rhs: List[int]
) -> List[int]:
    """
    Решает систему matrix @ x = rhs над GF(2) методом Гаусса.

    Параметры
    ----------
    matrix : List[List[int]]
        Матрица размера rows × cols, rows >= cols.
    rhs : List[int]
        Правая часть, длина = rows.

    Возвращает
    -------
    solution : List[int]
        Вектор-решение длины cols.
    """
    # Собираем расширенную матрицу
    rows, cols = len(matrix), len(matrix[0])
    augmented = [row[:] + [b] for row, b in zip(matrix, rhs)]
    pivot_row = 0

    # Прямой ход
    for col in range(cols):
        # найдём строку с 1 в этом столбце
        for r in range(pivot_row, rows):
            if augmented[r][col] == 1:
                augmented[pivot_row], augmented[r] = augmented[r], augmented[pivot_row]
                break
        else:
            continue

        # обнулим остальные единицы в этом столбце
        for r in range(rows):
            if r != pivot_row and augmented[r][col] == 1:
                for c in range(col, cols + 1):
                    augmented[r][c] ^= augmented[pivot_row][c]
        pivot_row += 1
        if pivot_row == cols:
            break

    # Обратный ход: читаем решение
    solution = [0] * cols
    for r in range(cols):
        lead = next((c for c in range(cols) if augmented[r][c] == 1), None)
        if lead is not None:
            solution[lead] = augmented[r][cols]
    return solution


def cyclic_shift(vec: list[Any], shifts: int) -> list[Any]:
    shifts %= len(vec)
    return vec[-shifts:] + vec[:-shifts]


class CyclicCodeService:
    @staticmethod
    def encode(
            message_bits: str,
            generator_matrix: List[List[int]]
    ) -> EncodedAndPolynomDTO:
        """
        Систематичное кодирование: кодовое слово c = m · G.

        Параметры
        ----------
        message_bits : str
            Битовая строка длины k, например "1101".
        generator_matrix : List[List[int]]
            Генераторная матрица G размером k×n.
        """
        # Выбираем из G те строки, где в m стоят «1»
        selected_rows = [
            row for bit, row in zip(message_bits, generator_matrix) if bit == "1"
        ]
        # Суммируем столбцы mod 2
        codeword_bits = [
            str(sum(col) % 2) for col in zip(*selected_rows)
        ]
        # Декларация полинома («x^i» для каждого «1» в m)
        terms = " + ".join(
            f"x^{i}" for i, bit in enumerate(message_bits) if bit == "1"
        )
        return EncodedAndPolynomDTO(terms, "".join(codeword_bits))

    @staticmethod
    def parse_generator_polynomial(poly_str: str) -> List[int]:
        """
        «x^3 + x + 1» → [1,0,1,1] (коэффициенты от x^0 к x^m).
        """
        coeffs: dict[int, int] = {}
        # разбиваем по «+» и «-»
        for term in re.split(r'\s*\+\s*|\s*-\s*', poly_str):
            if not term:
                continue
            if term == "x":
                power = 1
            elif "x^" in term:
                _, exp = term.split("x^", 1)
                power = int(exp)
            else:
                power = 0
            coeffs[power] = 1  # в GF(2) любой ненулевой = 1
        max_power = max(coeffs.keys(), default=0)
        return [coeffs.get(i, 0) for i in range(max_power + 1)]

    def decode(
            self,
            received_bits: str,
            generator_poly: str,
    ) -> str:
        """
        Декодирование по методу Мэггитта (burst‑trapping).

        Параметры
        ----------
        received_bits : str
            Принятое слово длины n.
        generator_poly : str
            Строковое представление g(x), например "x^3 + x + 1".
        """
        # 1) Подготовка входа
        codeword = np.array([int(b) for b in received_bits], dtype=int)
        n = codeword.size

        # g(x) → список от старшей к младшей
        g_coeffs = self.parse_generator_polynomial(generator_poly)
        divisor = np.array(list(reversed(g_coeffs)), dtype=int)
        m = divisor.size - 1

        generator_matrix: list[list[int]] = [g_coeffs.copy() + [0] * (n - len(g_coeffs))]

        for shift in range(m):
            row: list[int] = generator_matrix[-1]
            generator_matrix.append(cyclic_shift(row, 1))

        # 2) Инициализация регистров Мэггитта
        #    R — текущий код, S — текущий синдром длины m
        R = codeword.copy()
        _, rem = gf2_polynomial_division(R.tolist(), divisor.tolist())
        S = np.array(rem, dtype=int)
        pad_len = max(0, m - S.size)
        S = np.pad(S, (pad_len, 0), constant_values=0)

        # 3) Burst‑trapping: делаем n циклических сдвигов
        for _ in range(n):
            if S.any():
                # исправляем единичные ошибки по «1» в регистре синдрома
                error_positions = S.nonzero()[0]
                for pos in error_positions:
                    R[pos] ^= 1
                # пересчёт синдрома
                _, rem = gf2_polynomial_division(R.tolist(), divisor.tolist())
                S = np.array(rem, dtype=int)
                pad_len = max(0, m - S.size)
                S = np.pad(S, (pad_len, 0), constant_values=0)

            # один циклический сдвиг влево
            R = np.roll(R, -1)
            S = np.roll(S, -1)

        # 4) Восстановление информационного слова m из c = m · G
        #    Транспонируем G: получаем n×k, решаем GF(2)-систему
        GT = [list(col) for col in zip(*generator_matrix)]
        m_vector = gf2_solve_linear_system(GT, R.tolist())

        return "".join(str(bit) for bit in m_vector)
