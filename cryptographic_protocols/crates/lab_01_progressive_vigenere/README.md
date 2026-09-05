# Лабораторная №1 (2026): прогрессивный шифр Виженера

Условие: `docs/conditions/2026/лаба 1 Криптопротоколы.doc`.

Ключ сдвигается после каждого полного повторения: MODE → NPEF → OQFG.
Для номера буквы i от нуля: s = (key[i % L] + floor(i / L)) mod N.
Шифрование: c = (p + s) mod N. Расшифрование: p = (c + N − s) mod N.

Поддерживаются `en` (A–Z, 26 букв) и `ru` (А–Я с отдельной Ё, 33 буквы).
Регистр сохраняется. Не-буквы копируются и не расходуют ключ.
Буквы чужого алфавита отклоняются; смешанный русский и английский текст
в одном вызове не поддерживается. Ключ непустой, только из выбранного алфавита.
Каждый вызов начинает прогрессию с нуля; ключ нечувствителен к регистру.

Запуск из корня workspace:

```bash
cargo run -p lab_01_progressive_vigenere -- encrypt --alphabet en --key MODE --text CRYPTOGRAPHY
# OFBTGDKWOFME
cargo run -p lab_01_progressive_vigenere -- decrypt --alphabet en --key MODE --text OFBTGDKWOFME
# CRYPTOGRAPHY
cargo run -p lab_01_progressive_vigenere -- encrypt --alphabet ru --key КЛЮЧ --text КРИПТОГРАФИЯ
# ХЬЖЖЮЫВИМВИШ
cargo run -p lab_01_progressive_vigenere -- decrypt --alphabet ru --key КЛЮЧ --text ХЬЖЖЮЫВИМВИШ
# КРИПТОГРАФИЯ
just ci
```

По умолчанию INFO-логи показывают этапы, позиции и прогрессию блока.
`RUST_LOG=off` отключает логи и оставляет результат.

Отчёт: `docs/reports/2026/lab_01_progressive_vigenere/Ковалев Д.П. ВКБ43 1 лаба.docx`.
Пересборка отчёта с проверкой результатов реального CLI:

```bash
python3 scripts/lab_01_progressive_vigenere/build.py
```

Для генератора нужны `python-docx` и `lxml`. В отчёте есть формулы Word,
посимвольные таблицы шифрования и расшифрования, результаты запусков и листинг.
