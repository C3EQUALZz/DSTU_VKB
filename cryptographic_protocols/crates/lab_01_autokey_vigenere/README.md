# Лабораторная №1 (2026): шифр Виженера с самогенерирующимся ключом

Условие: `docs/conditions/2026/лаба 1 Криптопротоколы.doc`.

Начальный ключ продолжается буквами открытого текста: MODE + CRYPTOGR.
Для номера буквы i от нуля: s = key[i] при i < L, иначе s = plain[i − L].
При расшифровании продолжение ключа берётся из уже восстановленного текста.
Шифрование: c = (p + s) mod N. Расшифрование: p = (c + N − s) mod N.

Поддерживаются `en` (A–Z, 26 букв) и `ru` (А–Я с отдельной Ё, 33 буквы).
Регистр сохраняется. Не-буквы копируются и не расходуют ключ.
Буквы чужого алфавита отклоняются; смешанный русский и английский текст
в одном вызове не поддерживается. Ключ непустой, только из выбранного алфавита.
Каждый вызов начинает поток с начального ключа; ключ нечувствителен к регистру.

Запуск из корня workspace:

```bash
cargo run -p lab_01_autokey_vigenere -- encrypt --alphabet en --key MODE --text CRYPTOGRAPHY
# OFBTVFEGTDNP
cargo run -p lab_01_autokey_vigenere -- decrypt --alphabet en --key MODE --text OFBTVFEGTDNP
# CRYPTOGRAPHY
cargo run -p lab_01_autokey_vigenere -- encrypt --alphabet ru --key КЛЮЧ --text КРИПТОГРАФИЯ
# ХЬЖЖЭЯЛАТГЛП
cargo run -p lab_01_autokey_vigenere -- decrypt --alphabet ru --key КЛЮЧ --text ХЬЖЖЭЯЛАТГЛП
# КРИПТОГРАФИЯ
just ci
```

По умолчанию INFO-логи показывают этапы и позиции букв.
`RUST_LOG=off` отключает логи и оставляет результат.

Отчёт: `docs/reports/2026/lab_01_progressive_vigenere/Ковалев Д.П. ВКБ43 1 лаба.docx`.
Пересборка отчёта с проверкой результатов реального CLI:

```bash
python3 scripts/lab_01_progressive_vigenere/build.py
```

Для генератора нужны `python-docx` и `lxml`. В отчёте есть формулы Word,
посимвольные таблицы шифрования и расшифрования, результаты запусков и листинг.
