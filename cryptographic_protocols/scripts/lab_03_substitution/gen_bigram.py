"""Генерация биграммной лог-модели русского языка в виде Rust-константы.

Корпус — расшифрованные тексты лаб 4 (artifacts/lab_04_vigenere/corpus_ru.txt).
Результат пишется в crates/lab_03_substitution/src/domain/bigram_model.rs.
Запуск: python3 scripts/lab_03_substitution/gen_bigram.py
"""

from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALPHABET = list("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ") + ["_"]
IDX = {c: i for i, c in enumerate(ALPHABET)}
N = len(ALPHABET)


def norm(c: str) -> str:
    c = c.upper()
    return "Е" if c == "Ё" else c


def main() -> None:
    text = (ROOT / "artifacts" / "lab_04_vigenere" / "corpus_ru.txt").read_text(encoding="utf-8")
    cnt = [[1.0] * N for _ in range(N)]
    prev = None
    for ch in text:
        c = norm(ch)
        if c not in IDX:
            prev = None
            continue
        j = IDX[c]
        if prev is not None:
            cnt[prev][j] += 1
        prev = j
    rows = []
    for i in range(N):
        tot = sum(cnt[i])
        rows.append([round(math.log(cnt[i][j] / tot), 4) for j in range(N)])

    out = ROOT / "crates" / "lab_03_substitution" / "src" / "domain" / "bigram_model.rs"
    with out.open("w", encoding="utf-8") as f:
        f.write("//! Биграммная лог-модель русского языка (33×33), сгенерирована из корпуса.\n")
        f.write("//! Источник: расшифрованные тексты лаб 4 (~50 тыс. символов).\n")
        f.write("//! НЕ редактировать вручную — gen: scripts/lab_03_substitution/gen_bigram.py\n\n")
        f.write(f"pub const N: usize = {N};\n\n")
        f.write("pub const BIGRAM_LOGP: [[f64; 33]; 33] = [\n")
        for r in rows:
            f.write("    [" + ", ".join(f"{x}" for x in r) + "],\n")
        f.write("];\n")
    print(f"сгенерирован {out}")


if __name__ == "__main__":
    main()
