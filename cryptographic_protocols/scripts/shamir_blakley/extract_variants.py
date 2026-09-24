"""Извлечь варианты 1–20 таблицы 5.1 из локального PDF (нужен pdftotext)."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "docs/conditions/2026/72_Metod_Personalnaya_kiberbezopasnost_09_03_02_OFO_2022_1_4.pdf"
OUT = ROOT / "crates/shamir_blakley/data/variants.json"

SHAMIR_SHARE = re.compile(r"\{\s*(\d+)\s*;\s*(\d+)\s*\}")
BLAKLEY_COEFFS = re.compile(r"\{\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,")
BLAKLEY_VALUE = re.compile(r"(\d+)\s*\}")


def parse() -> list[dict]:
    result = subprocess.run(
        ["pdftotext", "-f", "116", "-l", "124", "-layout", str(PDF), "-"],
        check=True, text=True, capture_output=True,
    )
    sections = result.stdout.split("Схема Шамира")[1:]
    if len(sections) != 20:
        raise ValueError(f"Ожидалось 20 вариантов, найдено {len(sections)}")

    variants = []
    for number, section in enumerate(sections, start=1):
        shamir_matches = list(SHAMIR_SHARE.finditer(section))
        if len(shamir_matches) != 30:
            raise ValueError(f"Вариант {number}: ожидалось 30 долей Шамира, найдено {len(shamir_matches)}")
        shamir_rows = [
            [[int(value) for value in match.groups()] for match in shamir_matches[i:i + 6]]
            for i in range(0, 30, 6)
        ]
        if any(len({pair[0] for pair in row}) != 1 for row in shamir_rows):
            raise ValueError(f"Вариант {number}: x различается между символами")
        blakley_text = section[shamir_matches[-1].end():]
        triples = [[int(value) for value in match] for match in BLAKLEY_COEFFS.findall(blakley_text)]
        values = [int(value) for value in BLAKLEY_VALUE.findall(blakley_text)]
        if len(triples) != 30 or len(values) != 30:
            raise ValueError(f"Вариант {number}: ожидалось 30 долей Блэкли, найдено {len(triples)} и {len(values)}")
        coeff_rows = [triples[i:i + 6] for i in range(0, 30, 6)]
        if any(len({tuple(triple) for triple in row}) != 1 for row in coeff_rows):
            raise ValueError(f"Вариант {number}: коэффициенты плоскости различаются между символами")

        variants.append({
            "number": number,
            "shamir": {
                "x": [row[0][0] for row in shamir_rows],
                "values": [[row[column][1] for row in shamir_rows] for column in range(6)],
            },
            "blakley": {
                "coefficients": [row[0] for row in coeff_rows],
                "values": [[values[row * 6 + column] for row in range(5)] for column in range(6)],
            },
        })
    return variants


def main() -> None:
    variants = parse()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"variants": variants}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{OUT}: {len(variants)} вариантов")


if __name__ == "__main__":
    main()
