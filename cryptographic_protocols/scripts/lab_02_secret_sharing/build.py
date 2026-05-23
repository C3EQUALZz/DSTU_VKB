"""Генерация отчётов по лаб 2 для всех 28 вариантов."""

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
    add_listing,
    add_para,
    add_title_page,
    make_doc,
    save,
)

BIN = ROOT / "target" / "release" / "lab_02_secret_sharing"


def run_cli(*args: str) -> str:
    env = os.environ.copy()
    env["RUST_LOG"] = "error"
    res = subprocess.run(
        [str(BIN), *args],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    return res.stdout


def read_source(rel: str) -> str:
    return (ROOT / "crates" / "lab_02_secret_sharing" / "src" / rel).read_text(
        encoding="utf-8"
    )


def build_variant(variant: int) -> None:
    shamir_out = run_cli("shamir", "--variant", str(variant), "--dave-x", "2")
    blakley_out = run_cli("blakley", "--variant", str(variant))

    meta = LabMeta(
        number=2,
        title="Пороговые схемы разделения секрета Шамира и Блэкли",
        variant=variant,
    )
    doc = make_doc()
    add_title_page(doc, meta)
    doc.add_page_break()

    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: пороговые схемы разделения секрета — Шамира (на основе интерполяции "
        "Лагранжа в Z_p) и Блэкли (на основе пересечения плоскостей).",
    )
    add_para(
        doc,
        "Цель работы: освоить методы порогового разделения секрета между n участниками "
        "таким образом, чтобы для восстановления требовалось не менее m долей. "
        "Реализовать выполнение упражнений 2 и 3 методички для индивидуального варианта.",
    )

    add_heading(doc, "Краткие теоретические сведения", level=2)
    add_para(
        doc,
        "Схема Шамира. Секрет S — свободный член полинома f(x) ∈ Z_p[x] степени m − 1. "
        "Долей участника является пара (x_j, f(x_j)). По любым m долям секрет "
        "восстанавливается по формуле интерполяции Лагранжа в точке x = 0:",
    )
    add_para(
        doc,
        "f(0) = Σ_{j=1..m} f(x_j) · Π_{k≠j} (−x_k) · (x_j − x_k)^{-1}   (mod p)",
        indent=False,
    )
    add_para(
        doc,
        "Схема Блэкли. Секретом является координата x_0 точки Q = (x_0, y_0, z_0) "
        "в трёхмерном пространстве. Каждая доля — плоскость z = a·x + b·y + c, где "
        "c = z_0 − a·x_0 − b·y_0 (mod p). Любые три плоскости общего положения "
        "пересекаются в точке Q.",
    )

    add_heading(doc, "Задание варианта")
    add_para(
        doc,
        f"Вариант №{variant}. Решить упражнения 2 (Шамир) и 3 (Блэкли) по данным таблиц "
        "методички. В упражнении 2 — восстановить секрет и «правильную» долю Дейва "
        "(x = 2). В упражнении 3 — построить доли для четырёх участников (A, B, D, C) "
        "и восстановить секрет по первым трём (A, B, D).",
    )

    add_heading(doc, "Упражнение 2 — Шамир", level=2)
    add_para(
        doc,
        "Запустим программу для левой колонки (m = 4, p = 23) и правой колонки "
        "(m = 3, p = 31). В обоих случаях восстановим секрет f(0), полином и долю "
        "Дейва c x = 2:",
    )
    add_listing(
        doc,
        f"$ cargo run --release -p lab_02_secret_sharing -- shamir --variant {variant}\n"
        + shamir_out,
        caption=f"Листинг 1 — упражнение 2 для варианта {variant}",
    )

    add_heading(doc, "Упражнение 3 — Блэкли", level=2)
    add_para(
        doc,
        "Запустим программу для левой колонки (p = 17, Q = (15, 5, 4)) и правой "
        "колонки (p = 31, Q = (11, 10, 25)). Программа сгенерирует доли для "
        "участников A, B, D, C и восстановит секретную точку Q по любым трём:",
    )
    add_listing(
        doc,
        f"$ cargo run --release -p lab_02_secret_sharing -- blakley --variant {variant}\n"
        + blakley_out,
        caption=f"Листинг 2 — упражнение 3 для варианта {variant}",
    )

    add_heading(doc, "Ключевые модули реализации")
    add_para(
        doc,
        "Алгоритмы реализованы в crate lab_02_secret_sharing на Rust 2024 в архитектуре "
        "Clean Architecture: модулярная арифметика в Z_p выделена отдельно, схемы "
        "Шамира и Блэкли — независимые модули доменного слоя, прикладной слой "
        "оркестрирует выполнение упражнений по таблице вариантов.",
    )
    add_para(
        doc,
        "Листинг 3 — модулярная арифметика (src/domain/modular.rs):",
        indent=False,
    )
    add_listing(doc, read_source("domain/modular.rs"))
    add_para(doc, "Листинг 4 — схема Шамира (src/domain/shamir.rs):", indent=False)
    add_listing(doc, read_source("domain/shamir.rs"))
    add_para(doc, "Листинг 5 — схема Блэкли (src/domain/blakley.rs):", indent=False)
    add_listing(doc, read_source("domain/blakley.rs"))

    doc.add_page_break()
    add_heading(doc, "Выводы")
    add_para(
        doc,
        "В ходе работы реализованы две пороговые схемы разделения секрета: схема Шамира "
        "на интерполяции Лагранжа в Z_p и схема Блэкли на пересечении плоскостей в Z_p³. "
        "Корректность реализации подтверждается тестами на примерах 1, 2 и 3 из "
        "методички (для Шамира восстанавливается секрет 7 при p = 11; для Блэкли "
        "точка Q = (5, 1, 2) при p = 7 и Q = (10, 2, 3) при p = 11). Для всех 28 "
        "вариантов задание выполняется автоматически — программа возвращает секрет, "
        "коэффициенты полинома и легальную долю Дейва, а также восстанавливает Q "
        "по любым трём долям Блэкли.",
    )

    out = (
        ROOT
        / "docs"
        / "reports"
        / "lab_02_secret_sharing"
        / f"var_{variant:02d}"
        / f"Ковалев Д.П. ВКБ43 2 лаба.docx"
    )
    save(doc, out)
    print(f"  saved variant {variant:>2}: {out.relative_to(ROOT)}")


def main() -> None:
    if not BIN.exists():
        raise SystemExit(
            f"binary not built: run `cargo build -p lab_02_secret_sharing --release`"
        )
    for v in range(1, 29):
        build_variant(v)


if __name__ == "__main__":
    main()
