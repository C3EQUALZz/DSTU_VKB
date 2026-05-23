"""Чистые вычисления для лаб 2: Лагранж в Z_p, метод Гаусса, Блэкли."""

from __future__ import annotations


def mod_inv(a: int, p: int) -> int:
    a = a % p
    if a == 0:
        raise ValueError(f"inverse of 0 mod {p}")
    for k in range(1, p):
        if (a * k) % p == 1:
            return k
    raise ValueError(f"no inverse for {a} mod {p}")


def lagrange_zero(shares: list[tuple[int, int]], p: int):
    """Возвращает (f0, details). details = [(j, xj, yj, num_raw, num_mod, den_raw, den_mod, inv_den, lj0)]."""
    details = []
    total = 0
    for j, (xj, yj) in enumerate(shares):
        num_raw = 1
        den_raw = 1
        num_mod = 1
        den_mod = 1
        for k, (xk, _) in enumerate(shares):
            if k == j:
                continue
            num_raw *= -xk
            den_raw *= xj - xk
            num_mod = (num_mod * ((-xk) % p)) % p
            den_mod = (den_mod * ((xj - xk) % p)) % p
        inv_den = mod_inv(den_mod, p)
        lj0 = (num_mod * inv_den) % p
        details.append((j, xj, yj, num_raw, num_mod, den_raw, den_mod, inv_den, lj0))
        total = (total + yj * lj0) % p
    return total, details


def reconstruct_polynomial(shares: list[tuple[int, int]], p: int) -> list[int]:
    """Метод Гаусса для матрицы Вандермонда — возвращает (a_0, a_1, ..., a_{m-1})."""
    m = len(shares)
    mat = [[pow(x, k, p) for k in range(m)] + [y % p] for x, y in shares]
    for col in range(m):
        piv = next(r for r in range(col, m) if mat[r][col] != 0)
        mat[col], mat[piv] = mat[piv], mat[col]
        inv = mod_inv(mat[col][col], p)
        mat[col] = [(v * inv) % p for v in mat[col]]
        for r in range(m):
            if r == col or mat[r][col] == 0:
                continue
            f = mat[r][col]
            mat[r] = [(v - f * mat[col][i]) % p for i, v in enumerate(mat[r])]
    return [mat[i][m] for i in range(m)]


def blakley_c(a: int, b: int, q: tuple[int, int, int], p: int) -> int:
    x0, y0, z0 = q
    return (z0 - a * x0 - b * y0) % p


def gauss_blakley(planes: list[tuple[int, int, int]], p: int) -> tuple[int, int, int]:
    """planes — список (a, b, c). Возвращает (x, y, z) пересечения трёх плоскостей."""
    if len(planes) != 3:
        raise ValueError("need 3 planes")
    # ax + by - z = -c  →  расширенная матрица 3x4.
    mat = [[a % p, b % p, (-1) % p, (-c) % p] for a, b, c in planes]
    for col in range(3):
        piv = next((r for r in range(col, 3) if mat[r][col] != 0), None)
        if piv is None:
            raise ValueError("singular system")
        mat[col], mat[piv] = mat[piv], mat[col]
        inv = mod_inv(mat[col][col], p)
        mat[col] = [(v * inv) % p for v in mat[col]]
        for r in range(3):
            if r == col or mat[r][col] == 0:
                continue
            f = mat[r][col]
            mat[r] = [(v - f * mat[col][i]) % p for i, v in enumerate(mat[r])]
    return mat[0][3], mat[1][3], mat[2][3]


def gauss_blakley_first_valid(
    all_planes: list[tuple[int, int, int]], p: int
) -> tuple[tuple[int, int, int], tuple[int, ...]]:
    """Пробует тройки в порядке (0,1,2), (0,1,3), (0,2,3), (1,2,3) — возвращает (Q, combo)."""
    for combo in [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]:
        trio = [all_planes[i] for i in combo]
        try:
            return gauss_blakley(trio, p), combo
        except ValueError:
            continue
    raise ValueError("no valid combo")


def _format_row(row: list[int]) -> str:
    """Форматирует строку матрицы как «( v1, v2, v3 | v4 )»."""
    *coeffs, rhs = row
    coeff_part = ", ".join(str(v) for v in coeffs)
    return f"( {coeff_part} | {rhs} )"


def _format_matrix(mat: list[list[int]]) -> str:
    return "\n".join("    " + _format_row(r) for r in mat)


def gauss_with_steps(mat: list[list[int]], p: int) -> tuple[list[list[int]], list[str]]:
    """Гаусс-Жордан в Z_p с записью каждого шага.

    Принимает квадратную систему (n строк × (n+1) столбец), возвращает приведённую
    матрицу и список текстовых описаний шагов.
    """
    n = len(mat)
    mat = [row[:] for row in mat]
    steps: list[str] = [f"Начальная расширенная матрица:\n{_format_matrix(mat)}"]
    for col in range(n):
        piv = next((r for r in range(col, n) if mat[r][col] != 0), None)
        if piv is None:
            raise ValueError("singular system")
        if piv != col:
            mat[col], mat[piv] = mat[piv], mat[col]
            steps.append(
                f"Шаг {col + 1}.1. Меняем местами строки {col + 1} и {piv + 1} "
                f"(нужен ненулевой ведущий элемент в столбце {col + 1}):\n"
                f"{_format_matrix(mat)}"
            )
        inv = mod_inv(mat[col][col], p)
        old_pivot = mat[col][col]
        if inv != 1:
            mat[col] = [(v * inv) % p for v in mat[col]]
            steps.append(
                f"Шаг {col + 1}.2. Нормируем строку {col + 1}: умножаем на "
                f"{old_pivot}⁻¹ ≡ {inv} (mod {p}):\n{_format_matrix(mat)}"
            )
        for r in range(n):
            if r == col or mat[r][col] == 0:
                continue
            f = mat[r][col]
            mat[r] = [(v - f * mat[col][i]) % p for i, v in enumerate(mat[r])]
            steps.append(
                f"Шаг {col + 1}.3. Обнуляем элемент в строке {r + 1}, столбце {col + 1}: "
                f"строка {r + 1} ← строка {r + 1} − {f} · строка {col + 1} (mod {p}):\n"
                f"{_format_matrix(mat)}"
            )
    return mat, steps


def gauss_blakley_with_steps(
    planes: list[tuple[int, int, int]], p: int
) -> tuple[tuple[int, int, int], list[str]]:
    if len(planes) != 3:
        raise ValueError("need 3 planes")
    mat = [[a % p, b % p, (-1) % p, (-c) % p] for a, b, c in planes]
    reduced, steps = gauss_with_steps(mat, p)
    return (reduced[0][3], reduced[1][3], reduced[2][3]), steps


def gauss_vandermonde_with_steps(
    shares: list[tuple[int, int]], p: int
) -> tuple[list[int], list[str]]:
    m = len(shares)
    mat = [[pow(x, k, p) for k in range(m)] + [y % p] for x, y in shares]
    reduced, steps = gauss_with_steps(mat, p)
    coeffs = [reduced[i][m] for i in range(m)]
    return coeffs, steps
