"""Отчёт по лаб 5 — XOR-шифрование."""

from __future__ import annotations

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


def read_artifact(name: str) -> str:
    return (ROOT / "artifacts" / "lab_05_xor" / name).read_text(encoding="utf-8")


def read_source(rel: str) -> str:
    return (ROOT / "crates" / "lab_05_xor" / "src" / rel).read_text(encoding="utf-8")


def main() -> None:
    meta = LabMeta(number=5, title="Симметричное XOR-шифрование")
    doc = make_doc()
    add_title_page(doc, meta)
    doc.add_page_break()

    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: реализация симметричного XOR-шифрования текста с закрытым ключом.",
    )
    add_para(
        doc,
        "Цель работы: изучить математическую модель шифра на основе побитовой операции "
        "«исключающее ИЛИ» (XOR) и реализовать численный алгоритм его работы. "
        "Показать симметричность преобразования: одна и та же операция выполняет "
        "шифрование и дешифрование.",
    )

    add_heading(doc, "Краткие теоретические сведения", level=2)
    add_para(
        doc,
        "Операция XOR (⊕) задаётся таблицей истинности 0⊕0 = 0, 0⊕1 = 1, 1⊕0 = 1, 1⊕1 = 0. "
        "Шифрование байтового потока: c_i = p_i ⊕ k_{i mod L}, где L — длина ключа. "
        "В силу инволюции (a ⊕ b ⊕ b = a) повторное применение того же ключа возвращает "
        "исходный текст.",
    )
    add_para(
        doc,
        "Криптостойкость одноразового XOR-ключа равна стойкости использования: если "
        "длина ключа равна длине сообщения и ключ выбирается равновероятно, схема "
        "соответствует «шифру Вернама» и стойка по Шеннону. Короткий повторяющийся ключ "
        "уязвим к частотному анализу.",
    )

    add_heading(doc, "Программная реализация")
    add_para(
        doc,
        "Реализация выполнена на Rust в crate lab_05_xor по принципам Clean Architecture: "
        "доменная функция xor_stream обрабатывает байтовый поток с циклическим ключом, "
        "прикладной слой формирует отчёт с hex/dec-представлением, презентационный — clap-CLI.",
    )

    add_heading(doc, "Запуск и проверка работы программы", level=2)
    add_para(
        doc,
        "1. Демонстрация на эталонном примере из методички — четверостишие А. Блока с "
        "однобайтовым ключом K = 70:",
    )
    add_listing(
        doc,
        "$ cargo run --release -p lab_05_xor -- demo\n" + read_artifact("demo.txt"),
        caption="Листинг 1 — шифрование/дешифрование эталонного текста",
    )

    add_para(
        doc,
        "2. Шифрование произвольной русской строки однобайтовым ключом K = 73:",
    )
    add_listing(
        doc,
        "$ cargo run --release -p lab_05_xor -- encrypt \"Криптографические протоколы\" --key 73\n"
        + read_artifact("encrypt_phrase.txt"),
        caption="Листинг 2 — XOR-шифрование произвольной фразы",
    )

    add_heading(doc, "Листинг исходного кода")
    add_para(
        doc,
        "Листинг 3 — доменная реализация XOR (src/domain/xor.rs):",
        indent=False,
    )
    add_listing(doc, read_source("domain/xor.rs"))
    add_para(
        doc,
        "Листинг 4 — прикладной слой (src/application/usecases.rs):",
        indent=False,
    )
    add_listing(doc, read_source("application/usecases.rs"))

    doc.add_page_break()
    add_heading(doc, "Выводы")
    add_para(
        doc,
        "В ходе работы реализован простейший симметричный шифр на основе побитовой "
        "операции XOR. Корректность алгоритма подтверждается тестами на инволютивность "
        "(повторное применение того же ключа возвращает исходные данные) и на эталонном "
        "примере из методички (первый байт открытого текста ‘Н’ = 205, ключ 70 → "
        "шифробайт 139). Программа продемонстрировала корректную работу как для "
        "однобайтовых ключей, так и для многобайтовых строк.",
    )

    out = ROOT / "docs" / "reports" / "lab_05_xor" / "Ковалев Д.П. ВКБ43 5 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
