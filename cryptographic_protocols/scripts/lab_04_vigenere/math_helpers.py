"""Расчёты криптоанализа Виженера для отчёта: IC, χ², подбор ключа."""

from __future__ import annotations

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ_"  # 32 символа (Е=Ё, Ь=Ъ слиты в матрице)
# В нашем 33-символьном алфавите (shared) разделены, но для частот используем общий список.
RU_FREQ = {
    "_": 0.175, "О": 0.090, "Е": 0.072, "А": 0.062, "И": 0.062, "Т": 0.053,
    "Н": 0.053, "С": 0.045, "Р": 0.040, "В": 0.038, "Л": 0.035, "К": 0.028,
    "М": 0.026, "Д": 0.025, "П": 0.023, "У": 0.021, "Я": 0.018, "Ы": 0.016,
    "З": 0.016, "Ь": 0.014, "Б": 0.014, "Г": 0.013, "Ч": 0.012, "Й": 0.010,
    "Х": 0.009, "Ж": 0.007, "Ю": 0.006, "Ш": 0.006, "Ц": 0.004, "Щ": 0.003,
    "Э": 0.003, "Ф": 0.002, "Ё": 0.072, "Ъ": 0.014,
}
ALPH33 = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ"  # не используется напрямую
FULL33 = list("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ") + ["_"]
# Соберём 33-символьный алфавит как в shared::alphabet.
ALPHABET33 = [
    "А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О",
    "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э",
    "Ю", "Я", "_",
]
IDX = {c: i for i, c in enumerate(ALPHABET33)}
N = len(ALPHABET33)  # 33


def index_of_coincidence(seq: list[int]) -> float:
    n = len(seq)
    if n < 2:
        return 0.0
    counts = [0] * N
    for c in seq:
        counts[c] += 1
    s = sum(f * (f - 1) for f in counts)
    return s / (n * (n - 1))


def columns(text: list[int], key_len: int) -> list[list[int]]:
    cols: list[list[int]] = [[] for _ in range(key_len)]
    for i, c in enumerate(text):
        cols[i % key_len].append(c)
    return cols


def key_length_scores(text: list[int], lo: int, hi: int) -> list[tuple[int, float]]:
    out = []
    for L in range(lo, hi + 1):
        cols = columns(text, L)
        avg = sum(index_of_coincidence(c) for c in cols) / L
        out.append((L, avg))
    return out


def best_key_length(text: list[int], lo: int, hi: int, ratio: float = 0.95) -> int:
    scores = key_length_scores(text, lo, hi)
    mx = max(ic for _, ic in scores)
    for L, ic in scores:
        if ic >= mx * ratio:
            return L
    return scores[0][0]


def best_shift_for_column(col: list[int]) -> tuple[int, float]:
    """Возвращает (сдвиг, χ²) с минимальным χ² относительно частот русского языка."""
    n = len(col)
    counts = [0] * N
    for c in col:
        counts[c] += 1
    best_s, best_chi = 0, float("inf")
    for s in range(N):
        chi = 0.0
        for i in range(N):
            observed = counts[(i + s) % N]
            expected = RU_FREQ.get(ALPHABET33[i], 0.001) * n
            if expected > 1e-9:
                chi += (observed - expected) ** 2 / expected
        if chi < best_chi:
            best_chi, best_s = chi, s
    return best_s, best_chi


def to_indices(text: str) -> list[int]:
    return [IDX[c] for c in text if c in IDX]


def from_indices(idx: list[int]) -> str:
    return "".join(ALPHABET33[i % N] for i in idx)


def recover_key(text: list[int], key_len: int) -> tuple[str, list[tuple[int, int, float]]]:
    """Возвращает (ключ, [(номер столбца, сдвиг, χ²)])."""
    cols = columns(text, key_len)
    shifts = []
    key_chars = []
    for j, col in enumerate(cols):
        s, chi = best_shift_for_column(col)
        shifts.append((j + 1, s, chi))
        key_chars.append(ALPHABET33[s])
    return "".join(key_chars), shifts


def decrypt(text: list[int], key: str) -> str:
    k = to_indices(key)
    out = [(c - k[i % len(k)]) % N for i, c in enumerate(text)]
    return from_indices(out)
