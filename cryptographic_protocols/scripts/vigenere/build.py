"""Сборка отчёта: python3 scripts/vigenere/build.py.

Зависимости: python-docx, lxml; Rust/Cargo. Примеры выполняются реальным CLI.
"""
from pathlib import Path
import os
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import report_builder as rb
from docx.shared import Cm, Pt
from docx.oxml import OxmlElement

CRATE = 'vigenere'
OUT = ROOT / 'docs/reports/2026' / CRATE


def run(action, language, key, text, scheme):
    args = ['cargo', 'run', '--quiet', '-p', CRATE, '--', action,
            '--scheme', scheme, '--alphabet', language, '--key', key, '--text', text]
    result = subprocess.run(args, cwd=ROOT, env={**os.environ, 'RUST_LOG': 'off'},
                            text=True, capture_output=True, check=True)
    return shlex.join(args), result.stdout.rstrip('\n')


def main():
    rb.TEACHER = 'Дубровина А.С.'
    doc = rb.make_doc()
    for section in doc.sections:
        section.page_width, section.page_height = Cm(21), Cm(29.7)
    rb.add_title_page(doc, rb.LabMeta(1, 'Шифр Виженера'))
    for paragraph in doc.paragraphs:
        if paragraph.text == 'Проверил:':
            paragraph.runs[0].text = 'Проверила:'
    rb.add_page_break(doc)
    rb.add_heading(doc, '1. Тема, цель и задание')
    rb.add_para(doc, 'Тема: шифрование и расшифрование с помощью обычной, прогрессивной и самогенерирующейся схем Виженера. '
                'Цель: изучить многоалфавитную подстановку, реализовать её на Rust и проверить обратимость.')
    rb.add_para(doc, 'Задание из файла «docs/conditions/2026/лаба 1 Криптопротоколы.doc»: '
                'реализовать шифр Виженера (шифрование и расшифрование), используя прогрессивную схему, '
                'а также символы русского и латинского алфавитов.')
    rb.add_para(doc, 'Дополнительно реализованы обычная и самогенерирующаяся схемы. Все три схемы объединены в crate vigenere и сопоставлены на слове КРИПТОГРАФИЯ с ключом КЛЮЧ.')
    rb.add_heading(doc, '2. Анализ условия и алгоритм')
    rb.add_para(doc, 'В прогрессивной схеме каждая следующая копия ключа сдвигается на одну позицию '
                'в алфавите. Для MODE последовательность блоков: MODE, NPEF, OQFG. '
                'Первый блок имеет дополнительный сдвиг 0. Прогрессия меняется после полного блока ключа.')
    rb.add_para(doc, 'Принятые соглашения: английский алфавит ABCDEFGHIJKLMNOPQRSTUVWXYZ (26 букв); '
                'русский АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ (33 буквы). Ё и Е различаются. '
                'Алфавит выбирается явно. Во всех трёх схемах регистр сохраняется. Пробелы, цифры и пунктуация копируются '
                'без расходования ключа. Буквы другого алфавита отклоняются. Ключ непустой и содержит '
                'только буквы выбранного алфавита; его регистр не влияет на результат.')
    rb.add_para(doc, 'Единый crate vigenere содержит все три схемы. Параметр --alphabet ru-yo выбирает 33 русские буквы с отдельной Ё; --alphabet ru-no-yo выбирает алфавит лабораторной №4 без отдельной Ё, но со знаком _ для пробела. В этом алфавите Ё приводится к Е, а результат записывается в верхнем регистре. Взлом доступен для трёх схем и трёх алфавитов, а на коротких текстах его результат является статистической гипотезой.')
    rb.add_para(doc, 'Пусть N — размер алфавита, L — длина ключа, i — номер обрабатываемой буквы '
                '(от нуля), pᵢ и cᵢ — номера букв текста и шифротекста, kⱼ — номер буквы ключа. '
                'Номера букв также начинаются с нуля. Тогда:')
    sub = lambda name, idx: rb.m_sub(rb.m_text(name), rb.m_text(idx))
    for parts in [
        [rb.m_text('b'), rb.m_op(' = ⌊'), rb.m_frac(rb.m_text('i'), rb.m_text('L')), rb.m_op('⌋')],
        [sub('s','i'), rb.m_op(' = ('), sub('k','i mod L'), rb.m_op(' + b) mod N')],
        [sub('c','i'), rb.m_op(' = ('), sub('p','i'), rb.m_op(' + '), sub('s','i'), rb.m_op(') mod N')],
        [sub('p','i'), rb.m_op(' = ('), sub('c','i'), rb.m_op(' − '), sub('s','i'), rb.m_op(' + N) mod N')],
    ]:
        rb.add_math(doc, rb.omml_display(parts))
    rb.add_para(doc, 'Расшифрование вычитает тот же сдвиг, поэтому сложение и вычитание сокращаются '
                'по модулю N. Сначала ключ проверяется и переводится в индексы, затем текст обходится '
                'по символам Unicode. Сложность O(N·(T + L)), где T — число символов текста; '
                'для фиксированного алфавита она линейна. Память O(T + L + N), включая результат.')
    rb.add_heading(doc, '3. Расчёт примеров и результаты запуска')
    transcript = []
    for language, alphabet, plain, key, expected, scheme, scheme_name in [
        ('en', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'CRYPTOGRAPHY', 'MODE', 'OFBTGDKWOFME', 'progressive', 'Прогрессивная схема'),
        ('ru-yo', 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'КРИПТОГРАФИЯ', 'КЛЮЧ', 'ХЬЖЖЮЫВИМВИШ', 'progressive', 'Прогрессивная схема'),
        ('ru-yo', 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'КРИПТОГРАФИЯ', 'КЛЮЧ', 'ХЬЖЖЭЪБЗКАЖЦ', 'standard', 'Обычная схема'),
        ('ru-yo', 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'КРИПТОГРАФИЯ', 'КЛЮЧ', 'ХЬЖЖЭЯЛАТГЛП', 'autokey', 'Самогенерирующийся ключ'),
    ]:
        rb.add_heading(doc, f'{scheme_name}: {plain}, ключ {key}', level=2)
        if scheme != 'progressive':
            autokey = scheme == 'autokey'
            stream = (key + plain)[:len(plain)] if autokey else (key * ((len(plain)+len(key)-1)//len(key)))[:len(plain)]
            rb.add_para(doc, f'Открытый текст: {plain}. Ключевая последовательность: {stream}. N = 33, L = 4.')
            if autokey:
                rb.add_math(doc, rb.omml_display([sub('s','i'), rb.m_op(' = '), sub('k','i'), rb.m_text(', 0 ≤ i < L')]))
                rb.add_math(doc, rb.omml_display([sub('s','i'), rb.m_op(' = '), sub('p','i − L'), rb.m_text(', i ≥ L')]))
                rb.add_para(doc, 'После начального ключа используются буквы исходного текста. При расшифровании они восстанавливаются последовательно: сначала первые четыре буквы КРИП, затем они служат ключом для следующих четырёх букв. Шифротекст в продолжение ключа не включается. Пробелы и пунктуация не пополняют ключ.')
            else:
                rb.add_math(doc, rb.omml_display([sub('s','i'), rb.m_op(' = '), sub('k','i mod L')]))
                rb.add_para(doc, 'Ключ КЛЮЧ повторяется без изменения; дополнительного сдвига блока нет.')
            rb.add_math(doc, rb.omml_display([sub('c','i'), rb.m_op(' = ('), sub('p','i'), rb.m_op(' + '), sub('s','i'), rb.m_op(') mod 33')]))
            rb.add_math(doc, rb.omml_display([sub('p','i'), rb.m_op(' = ('), sub('c','i'), rb.m_op(' − '), sub('s','i'), rb.m_op(' + 33) mod 33')]))
        rb.add_para(doc, 'В таблице приведены индексы букв, дополнительный сдвиг блока, '
                    'эффективная буква ключа и результаты обеих операций. Все остатки неотрицательные.')
        table = doc.add_table(rows=1, cols=7)
        table.style = 'Table Grid'
        for cell, value in zip(table.rows[0].cells, ['i', 'Буква / p', 'b', 'Ключ / s', 'p+s mod N', 'Шифр', 'c−s mod N']):
            cell.text = value
        table.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
        calculated = ''
        for i, char in enumerate(plain):
            p = alphabet.index(char)
            b = i // len(key) if scheme == 'progressive' else 0
            source = plain[i-len(key)] if scheme == 'autokey' and i >= len(key) else key[i % len(key)]
            s = (alphabet.index(source) + b) % len(alphabet)
            c = (p + s) % len(alphabet)
            calculated += alphabet[c]
            values = [str(i), f'{char} / {p}', str(b), f'{alphabet[s]} / {s}',
                      str(c), alphabet[c], f'{(c-s) % len(alphabet)} / {char}']
            for cell, value in zip(table.add_row().cells, values):
                cell.text = value
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraph.paragraph_format.first_line_indent = Cm(0)
                    paragraph.paragraph_format.line_spacing = 1
                    for run_text in paragraph.runs:
                        run_text.font.size = Pt(10)
        assert calculated == expected
        enc_cmd, encrypted = run('encrypt', language, key, plain, scheme)
        enc_output = encrypted
        dec_cmd, decrypted = run('decrypt', language, key, encrypted, scheme)
        dec_output = decrypted
        assert encrypted == expected and decrypted == plain
        rb.add_para(doc, f'Шифрование: {plain} → {encrypted}. Расшифрование: {encrypted} → {decrypted}.')
        for command, result in [(enc_cmd, enc_output), (dec_cmd, dec_output)]:
            # Короткие строки команд помещаются в ширину страницы.
            shown = command.replace(' --alphabet', ' \\\n  --alphabet').replace(' --text', ' \\\n  --text')
            rb.add_listing(doc, '$ ' + shown + '\n' + result)
            transcript.append('$ ' + command + '\n' + result)
    rb.add_para(doc, 'Выше приведён фактический стандартный вывод программы. Для краткости '
                'при сборке отчёта установлен RUST_LOG=off; обычный запуск показывает этапы и номера блоков.')
    rb.add_heading(doc, 'Сопоставление трёх схем', level=2)
    for label, stream, cipher in [
        ('Обычная', 'КЛЮЧКЛЮЧКЛЮЧ', 'ХЬЖЖЭЪБЗКАЖЦ'),
        ('Прогрессивная', 'КЛЮЧЛМЯШМНАЩ', 'ХЬЖЖЮЫВИМВИШ'),
        ('Самогенерирующаяся', 'КЛЮЧКРИПТОГР', 'ХЬЖЖЭЯЛАТГЛП'),
    ]:
        rb.add_para(doc, f'{label}: ключ {stream}; шифротекст {cipher}; восстановленный текст КРИПТОГРАФИЯ.')
    rb.add_para(doc, 'Первые четыре буквы шифротекста совпадают, потому что все схемы начинают с одного ключа КЛЮЧ. Затем последовательности ключа расходятся.')
    rb.add_heading(doc, '4. Реализация и проверка')
    rb.add_para(doc, 'Единый crate vigenere включён в Cargo workspace. '
                'domain содержит алфавиты, схемы и криптоанализ; application разбит по трём схемам; '
                'infrastructure реализует порт вывода; presentation содержит единый CLI на clap. '
                'Ошибки возвращаются через thiserror и color-eyre. Полный ключ в журнал не записывается.')
    rb.add_para(doc, 'Тесты проверяют пример методички, русский пример, пустой текст, регистр, '
                'пунктуацию, циклический переход Z→A и Я→А, недопустимые ключи и чужие буквы. '
                'Proptest генерирует тексты и ключи для обоих алфавитов и проверяет сохранение длины '
                'и равенство D(E(M)) = M. Команда полной проверки проекта: just ci.')
    rb.add_para(doc, 'Для самогенерирующейся схемы кольцевой буфер длины L начинается ключом и затем хранит индексы исходных (при расшифровании — восстановленных) букв. Он создаётся заново при каждом вызове. Сложность O(N·(T + L)), память O(T + L + N) с результатом; дополнительная память потока O(L).')
    rb.add_para(doc, 'Обычная схема повторяет ключ; прогрессивная добавляет номер блока; самогенерирующаяся продолжает ключ открытым текстом. Все три схемы работают с en, ru-yo и ru-no-yo. Тесты проверяют русский пример, отдельную Ё, алфавит без Ё, регистр, пунктуацию, ошибки ввода и proptest roundtrip.')
    rb.add_heading(doc, '5. Листинг ключевого Rust-кода')
    rb.add_heading(doc, 'Единый алгоритм трёх схем', level=2)
    rb.add_listing(doc, (ROOT / 'crates' / CRATE / 'src/domain/scheme.rs').read_text())
    rb.add_heading(doc, '6. Выводы')
    rb.add_para(doc, 'Для слова КРИПТОГРАФИЯ с ключом КЛЮЧ выполнены все три варианта: обычный — ХЬЖЖЭЪБЗКАЖЦ, прогрессивный — ХЬЖЖЮЫВИМВИШ, самогенерирующийся — ХЬЖЖЭЯЛАТГЛП. Каждый результат расшифрован обратно. Обычная схема повторяет ключ, прогрессивная сдвигает его блоки, самогенерирующаяся продолжает ключ открытым текстом. Все схемы рассматриваются как учебные.')
    rb.add_para(doc, 'Реализованы шифрование и расшифрование по прогрессивной схеме Виженера '
                'для латиницы и кириллицы. Результат английского примера совпадает с условием. '
                'Посимвольный расчёт русского примера учитывает отдельную букву Ё. '
                'Обратное преобразование восстанавливает исходное слово. Прогрессия убирает '
                'повторение неизменного короткого ключа, однако расписание сдвигов остаётся '
                'предсказуемым и повторяется через N·L букв; схема служит учебным примером.')
    for table in doc.tables:
        for row in table.rows:
            row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
    for paragraph in doc.paragraphs:
        if paragraph.runs and all(run.bold for run in paragraph.runs):
            paragraph.paragraph_format.keep_with_next = True
    rb.save(doc, OUT / 'Ковалев Д.П. ВКБ43 1 лаба.docx')
    (OUT / 'examples.txt').write_text('\n\n'.join(transcript) + '\n')
    print(OUT / 'Ковалев Д.П. ВКБ43 1 лаба.docx')


if __name__ == '__main__':
    main()
