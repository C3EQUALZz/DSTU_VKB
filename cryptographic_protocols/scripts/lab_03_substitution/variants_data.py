"""Загрузка шифртекстов 20 вариантов лаб 3 из artifacts/lab_03_substitution/cipher_texts/."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CIPHER_DIR = ROOT / "artifacts" / "lab_03_substitution" / "cipher_texts"


def load_variant(n: int) -> str:
    path = CIPHER_DIR / f"var_{n:02d}.txt"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


VARIANTS = {n: load_variant(n) for n in range(1, 21)}
