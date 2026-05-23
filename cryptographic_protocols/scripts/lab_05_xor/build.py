"""Отчёт по лаб 5 — XOR с полным ручным решением."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from report_builder import (  # noqa: E402
    LabMeta,
    add_heading,
    add_listing,
    add_math,
    add_page_break,
    add_para,
    add_qa,
    add_title_page,
    make_doc,
    save,
)


def read_artifact(name: str) -> str:
    return (ROOT / "artifacts" / "lab_05_xor" / name).read_text(encoding="utf-8")


def read_source(rel: str) -> str:
    return (ROOT / "crates" / "lab_05_xor" / "src" / rel).read_text(encoding="utf-8")


KEY = 70  # 0b01000110


def encode_win1251(s: str) -> list[int]:
    return list(s.encode("cp1251"))


def to_bits(n: int) -> str:
    return f"{n:08b}"


def manual_xor_first_letters(stanza: str, n: int = 6) -> str:
    """Подробная таблица XOR для первых n символов."""
    codes = encode_win1251(stanza)[:n]
    lines = [f"Ключ K = {KEY} = {to_bits(KEY)} (1 байт).", ""]
    lines.append("Шифрование c_i = p_i ⊕ K:")
    for i, c in enumerate(codes):
        sym = stanza[i]
        xor = c ^ KEY
        lines.append(
            f"  i={i:>2}  '{sym}' = {c:>3} = {to_bits(c)}  ⊕  {to_bits(KEY)}  =  "
            f"{to_bits(xor)} = {xor:>3}"
        )
    return "\n".join(lines)


CONTROL_QA = [
    (
        "Опишите методику шифрования с закрытым ключом.",
        "Симметричное шифрование: отправитель и получатель используют один и тот же "
        "секретный ключ. Шифрование E_K(P) = C, дешифрование D_K(C) = P. Ключ передаётся "
        "по защищённому каналу заранее (out-of-band) или согласуется протоколом обмена "
        "(например, Диффи-Хеллманом).",
    ),
    (
        "Опишите логическую операцию XOR.",
        "XOR (⊕) — побитовое сложение по модулю 2. Таблица истинности: 0⊕0 = 0, 0⊕1 = 1, "
        "1⊕0 = 1, 1⊕1 = 0. Операция ассоциативна, коммутативна и обратима: "
        "a ⊕ b ⊕ b = a (инволюция).",
    ),
    (
        "Механизм работы шифрования на основе XOR.",
        "Для каждого байта открытого текста p_i и циклически повторяющегося ключа k_{i mod L} "
        "вычисляется c_i = p_i ⊕ k_{i mod L}. Дешифрование — та же операция: "
        "p_i = c_i ⊕ k_{i mod L}. Шифр обратим без отдельной процедуры расшифрования.",
    ),
    (
        "Насколько надёжен XOR-шифр?",
        "Если ключ длиннее или равен длине сообщения и используется только один раз "
        "(one-time pad / шифр Вернама) — теоретически невзламываем (Шеннон). С повторяющимся "
        "коротким ключом — крайне уязвим к частотному анализу и атаке «известный открытый "
        "текст» (XOR двух шифровок убирает ключ). На практике XOR применяется как "
        "вспомогательная операция в потоковых шифрах (RC4) и в режимах работы (CTR, OFB).",
    ),
]


def main() -> None:
    meta = LabMeta(number=5, title="Симметричное XOR-шифрование")
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

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

    add_heading(doc, "Теоретические сведения", level=2)
    add_para(
        doc,
        "Операция XOR задаётся таблицей истинности 0⊕0 = 0, 0⊕1 = 1, 1⊕0 = 1, 1⊕1 = 0. "
        "Шифрование байтового потока:",
    )
    from report_builder import m_op, m_sub, m_text, omml_display

    add_math(
        doc,
        omml_display([
            m_sub(m_text("c"), m_text("i")),
            m_op(" = "),
            m_sub(m_text("p"), m_text("i")),
            m_op(" ⊕ "),
            m_sub(m_text("k"), m_text("i mod L")),
        ]),
    )
    add_para(
        doc,
        "В силу инволюции (a ⊕ b ⊕ b = a) повторное применение того же ключа возвращает "
        "исходный текст: D_K(E_K(P)) = P.",
    )

    add_heading(doc, "Ручное решение примера из методички")
    stanza = (
        "Ночь, улица, фонарь, аптека,\n"
        "Бессмысленный и тусклый свет.\n"
        "Живи ещё хоть четверть века —\n"
        "Всё будет так. Исхода нет."
    )
    add_para(doc, "Исходный текст (четверостишие А. Блока):")
    for line in stanza.split("\n"):
        add_para(doc, line, indent=False)
    add_para(doc, "Ключ: K = 70 (десятичное), что в двоичной записи 01000110.")
    add_para(
        doc,
        "Покажем шаги XOR-шифрования для первых 6 символов первой строки. Кодировка — "
        "Windows-1251 (1 байт на букву кириллицы):",
    )
    add_listing(doc, manual_xor_first_letters(stanza, n=6))
    add_para(
        doc,
        "Аналогично шифруются остальные байты. Для дешифрования применяется та же операция "
        "к шифртексту с тем же ключом — благодаря инволютивности XOR (a ⊕ K ⊕ K = a) "
        "получаем исходный байт.",
    )

    add_page_break(doc)
    add_heading(doc, "Программная проверка")
    add_listing(
        doc,
        "$ cargo run --release -p lab_05_xor -- demo\n" + read_artifact("demo.txt"),
        caption="Листинг 1 — шифрование и дешифрование эталонного текста",
    )
    add_listing(
        doc,
        "$ cargo run --release -p lab_05_xor -- encrypt \"Криптографические протоколы\" --key 73\n"
        + read_artifact("encrypt_phrase.txt"),
        caption="Листинг 2 — XOR-шифрование произвольной фразы",
    )

    add_page_break(doc)
    add_heading(doc, "Контрольные вопросы")
    for i, (q, a) in enumerate(CONTROL_QA, start=1):
        add_qa(doc, i, q, a)

    add_page_break(doc)
    add_heading(doc, "Выводы")
    add_para(
        doc,
        "В ходе работы реализован простейший симметричный шифр на основе побитовой "
        "операции XOR. Ручное вычисление для первых шести символов стиха А. Блока с "
        "ключом K = 70 (например, 'Н' = 205 = 11001101 → 205 ⊕ 70 = 139 = 10001011) "
        "совпадает с программным выводом. Корректность реализации подтверждается "
        "тестами на инволютивность и эталонным примером методички. XOR с однобайтовым "
        "повторяющимся ключом небезопасен в чистом виде, но является основой для "
        "потоковых шифров.",
    )

    add_page_break(doc)
    add_heading(doc, "Листинг исходного кода")
    for caption, rel in [
        ("Листинг 3 — доменная реализация XOR (src/domain/xor.rs)", "domain/xor.rs"),
        ("Листинг 4 — прикладной слой (src/application/usecases.rs)", "application/usecases.rs"),
        ("Листинг 5 — CLI (src/presentation/cli.rs)", "presentation/cli.rs"),
    ]:
        add_listing(doc, read_source(rel), caption=caption)

    out = ROOT / "docs" / "reports" / "lab_05_xor" / "Ковалев Д.П. ВКБ43 5 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
