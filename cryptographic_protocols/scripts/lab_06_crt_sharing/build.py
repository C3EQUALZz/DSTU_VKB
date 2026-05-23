"""Отчёты по лаб 6 — Миньотта + Асмут-Блум, 20 вариантов."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from report_builder import (  # noqa: E402
    LabMeta,
    add_heading,
    add_label,
    add_listing,
    add_math,
    add_para,
    add_title_page,
    m_frac,
    m_op,
    m_prod,
    m_sub,
    m_sum,
    m_text,
    make_doc,
    omml_display,
    save,
)

BIN = ROOT / "target" / "release" / "lab_06_crt_sharing"
VARIANTS = [
    "АНКЛАВ", "АРМАДА", "БЕСЕДА", "БЕСИТЬ", "ВЗВЕСЬ", "ВЗГЛЯД", "ГЕКТАР", "ГЕЙЗЕР", "ДЕВИЦА",
    "ДЕКАДА", "ЗАДАТЬ", "ЗАЖАТЬ", "ЗАМЯТЬ", "ИНТЕРН", "КАПКАН", "КАПРОН", "ЛЕКАРЬ", "ЛЕКТОР",
    "НАДЗОР", "НАДРЕЗ",
]


def run_cli(variant: int) -> str:
    env = os.environ.copy()
    env["RUST_LOG"] = "error"
    res = subprocess.run(
        [str(BIN), "variant", "--variant", str(variant), "--k", "3", "--n", "5", "--r", "7"],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    return res.stdout


def read_source(rel: str) -> str:
    return (ROOT / "crates" / "lab_06_crt_sharing" / "src" / rel).read_text(encoding="utf-8")


def build_variant(variant: int) -> None:
    word = VARIANTS[variant - 1]
    output = run_cli(variant)

    meta = LabMeta(
        number=6,
        title=f"Пороговые схемы Миньотта и Асмут-Блума для слова «{word}»",
        variant=variant,
    )
    doc = make_doc()
    add_title_page(doc, meta)
    doc.add_page_break()

    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: пороговые схемы разделения секрета на основе системы остаточных классов "
        "(СОК) — схемы Миньотта и Асмута-Блума.",
    )
    add_para(
        doc,
        "Цель работы: освоить принципы порогового разделения данных, реализовать обе "
        "схемы для слова варианта, продемонстрировать восстановление секрета как по k "
        "долям, так и по n долям.",
    )

    add_heading(doc, "Теоретические сведения", level=2)
    add_para(
        doc,
        "Схема Миньотта. Для (k, n)-разделения подбирается последовательность взаимно "
        "простых чисел p₁ < p₂ < ... < pₙ, для которой выполняется неравенство:",
    )
    # β = ∏_{i=0..k-2} p_{n-i}   <   S   <   α = ∏_{i=1..k} p_i
    add_math(
        doc,
        omml_display([
            m_prod(m_text("i") + m_op("=0"), m_text("k") + m_op("−2"),
                   m_sub(m_text("p"), m_text("n") + m_op("−") + m_text("i"))),
            m_op(" < "), m_text("S"), m_op(" < "),
            m_prod(m_text("i") + m_op("=1"), m_text("k"),
                   m_sub(m_text("p"), m_text("i"))),
        ]),
    )
    add_para(
        doc,
        "Доли участников α_i = S mod p_i. По любым k долям секрет S восстанавливается через "
        "Китайскую теорему об остатках:",
        indent=False,
    )
    # CRT: S = sum_i a_i * P_i * P_i^{-1}_{p_i} mod P
    add_math(
        doc,
        omml_display([
            m_text("S"), m_op(" = "),
            m_sum(m_text("i") + m_op("=1"), m_text("k"),
                  m_sub(m_text("α"), m_text("i")) + m_op(" · ") +
                  m_sub(m_text("P"), m_text("i")) + m_op(" · ") +
                  m_sub(m_text("M"), m_text("i"))),
            m_op(" (mod "), m_text("P"), m_op(")"),
        ]),
    )
    add_para(
        doc,
        "где P = ∏ pᵢ, Pᵢ = P / pᵢ, Mᵢ = Pᵢ⁻¹ mod pᵢ.",
        indent=False,
    )

    add_para(
        doc,
        "Схема Асмут-Блума. Дополнительно к базису берётся простое q > S и случайное r. "
        "Доли вычисляются по числу S′ = S + r·q, восстановление CRT даёт S′, после чего "
        "S = S′ mod q. Условие на параметры:",
    )
    # ∏_{i=1..k} p_i  >  q · ∏_{i=0..k-2} p_{n-i}
    add_math(
        doc,
        omml_display([
            m_prod(m_text("i") + m_op("=1"), m_text("k"),
                   m_sub(m_text("p"), m_text("i"))),
            m_op(" > "), m_text("q"), m_op(" · "),
            m_prod(m_text("i") + m_op("=0"), m_text("k") + m_op("−2"),
                   m_sub(m_text("p"), m_text("n") + m_op("−") + m_text("i"))),
        ]),
    )

    add_heading(doc, "Задание варианта")
    add_para(
        doc,
        f"Вариант №{variant}: слово «{word}». Реализовать (k=3, n=5) пороговые схемы "
        "Миньотта и Асмута-Блума, показать процесс разделения и восстановления, восстановить "
        "слово как по k долям, так и по всем n долям.",
    )
    add_para(
        doc,
        "В реализации каждая буква слова обрабатывается как отдельный малый секрет — "
        "индекс буквы в 33-буквенном алфавите со смещением +250 (чтобы гарантированно "
        "выполнялось β < S < α для базиса [5, 7, 11, 13, 17]).",
    )

    add_heading(doc, "Программная реализация", level=2)
    add_para(
        doc,
        "Решение оформлено как Cargo-workspace на Rust 2024 в crate lab_06_crt_sharing "
        "по принципам Clean Architecture: домен (Миньотта, Асмут-Блум, CRT, кодировка), "
        "прикладной слой (сценарий обработки слова), CLI (clap). Длинная арифметика — "
        "num-bigint, модулярная инверсия — расширенный алгоритм Евклида.",
    )

    add_heading(doc, "Запуск программы", level=2)
    add_para(
        doc,
        f"Запуск для варианта {variant}:",
    )
    add_listing(
        doc,
        f"$ cargo run --release -p lab_06_crt_sharing -- variant --variant {variant} --k 3 --n 5 --r 7\n"
        + output,
        caption=f"Листинг 1 — выполнение варианта {variant}",
    )

    add_heading(doc, "Листинг ключевых модулей")
    add_para(doc, "Листинг 2 — реализация CRT (src/domain/crt.rs):", indent=False)
    add_listing(doc, read_source("domain/crt.rs"))
    add_para(doc, "Листинг 3 — схема Миньотта (src/domain/mignotte.rs):", indent=False)
    add_listing(doc, read_source("domain/mignotte.rs"))
    add_para(doc, "Листинг 4 — схема Асмута-Блума (src/domain/asmuth_bloom.rs):", indent=False)
    add_listing(doc, read_source("domain/asmuth_bloom.rs"))

    doc.add_page_break()
    add_heading(doc, "Выводы")
    add_para(
        doc,
        "В ходе работы реализованы пороговые схемы Миньотта и Асмута-Блума на системе "
        "остаточных классов. Корректность подтверждается тестами на примерах из методички "
        "(для секрета S=250, k=3, n=5, базиса [5, 7, 11, 13, 17] обе схемы корректно "
        "восстанавливают исходное значение через CRT). Для всех 20 слов варианта "
        f"(включая «{word}») восстановление по k=3 долям и по всем n=5 долям возвращает "
        "исходный код буквы, а итоговое восстановленное слово совпадает с исходным.",
    )

    out = (
        ROOT
        / "docs"
        / "reports"
        / "lab_06_crt_sharing"
        / f"var_{variant:02d}"
        / f"Ковалев Д.П. ВКБ43 6 лаба.docx"
    )
    save(doc, out)
    print(f"  saved variant {variant:>2}: {out.relative_to(ROOT)}")


def main() -> None:
    if not BIN.exists():
        raise SystemExit(
            "binary not built: run `cargo build -p lab_06_crt_sharing --release`"
        )
    for v in range(1, 21):
        build_variant(v)


if __name__ == "__main__":
    main()
