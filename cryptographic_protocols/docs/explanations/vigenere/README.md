# Шифр Виженера — запуск и проверка

Все команды ниже выполняются из корня `cryptographic_protocols`. Для работы №1
за 2026 год и лабораторной №4 за 2025 год используется один крейт `vigenere`.
Старые имена `lab_01_progressive_vigenere`, `lab_01_autokey_vigenere` и
`lab_04_vigenere` в команде `cargo run -p` больше не используются.

## Шифрование и расшифрование

Форма команды:

```bash
cargo run --quiet -p vigenere -- encrypt --scheme СХЕМА --alphabet АЛФАВИТ --key КЛЮЧ --text ТЕКСТ
cargo run --quiet -p vigenere -- decrypt --scheme СХЕМА --alphabet АЛФАВИТ --key КЛЮЧ --text ШИФРОТЕКСТ
```

`--scheme` принимает `standard` (ключ повторяется), `progressive` (после
каждого полного блока ключа сдвиг увеличивается на единицу) или `autokey`
(после начального ключа используются буквы открытого текста).

Три схемы на одном русском примере:

```bash
cargo run --quiet -p vigenere -- encrypt --scheme standard --alphabet ru-yo --key 'КЛЮЧ' --text 'КРИПТОГРАФИЯ'
# ХЬЖЖЭЪБЗКАЖЦ
cargo run --quiet -p vigenere -- decrypt --scheme standard --alphabet ru-yo --key 'КЛЮЧ' --text 'ХЬЖЖЭЪБЗКАЖЦ'
# КРИПТОГРАФИЯ

cargo run --quiet -p vigenere -- encrypt --scheme progressive --alphabet ru-yo --key 'КЛЮЧ' --text 'КРИПТОГРАФИЯ'
# ХЬЖЖЮЫВИМВИШ
cargo run --quiet -p vigenere -- decrypt --scheme progressive --alphabet ru-yo --key 'КЛЮЧ' --text 'ХЬЖЖЮЫВИМВИШ'
# КРИПТОГРАФИЯ

cargo run --quiet -p vigenere -- encrypt --scheme autokey --alphabet ru-yo --key 'КЛЮЧ' --text 'КРИПТОГРАФИЯ'
# ХЬЖЖЭЯЛАТГЛП
cargo run --quiet -p vigenere -- decrypt --scheme autokey --alphabet ru-yo --key 'КЛЮЧ' --text 'ХЬЖЖЭЯЛАТГЛП'
# КРИПТОГРАФИЯ
```

Для латинского алфавита в задании 2026 года:

```bash
cargo run --quiet -p vigenere -- encrypt --scheme progressive --alphabet en --key MODE --text CRYPTOGRAPHY
# OFBTGDKWOFME
cargo run --quiet -p vigenere -- decrypt --scheme progressive --alphabet en --key MODE --text OFBTGDKWOFME
# CRYPTOGRAPHY
```

## Алфавиты и текст

| Значение `--alphabet` | Состав и поведение |
|---|---|
| `en` | 26 латинских букв. |
| `ru-yo` | 33 русские буквы, `Ё` — отдельная буква. |
| `ru-no-yo` | 32 русские буквы и `_` как символ алфавита; `Ё` приводится к `Е`, результат выводится в верхнем регистре. Этот вариант использует лабораторная №4. |

Все три схемы работают с каждым алфавитом. Пробелы и знаки препинания
сохраняются и не расходуют ключ; в `ru-no-yo` знак `_` расходует ключ, поскольку
входит в алфавит. Буквы другого алфавита вызывают ошибку. Ключ должен состоять
из символов выбранного алфавита. Текст с пробелами заключайте в кавычки.

Например, для `ru-no-yo`:

```bash
cargo run --quiet -p vigenere -- encrypt --scheme standard --alphabet ru-no-yo --key 'А' --text 'ЕЁ_!'
# ЕЕ_!
```

## Криптоанализ

`break` принимает шифротекст позиционным аргументом, затем схему, алфавит и
диапазон **длин начального ключа**. Команда выводит наиболее вероятный ключ,
длину, статистическую оценку и расшифрованный текст.

Для готового шифротекста варианта 11 лабораторной №4:

```bash
cipher=$(tr -d '\r\n' < artifacts/lab_04_vigenere/cipher_texts/var_11.txt)
RUST_LOG=warn cargo run --quiet -p vigenere -- break "$cipher" \
  --scheme standard --alphabet ru-no-yo --min-key 2 --max-key 8
# Восстановленный ключ: ДВОР
```

Для прогрессивной и самогенерирующейся схем можно создать проверочный
шифротекст из первых 800 символов текста варианта 11 и передать его в `break`:

```bash
plain=$(python3 -c 'from pathlib import Path; print(Path("artifacts/lab_04_vigenere/var_11/plaintext.txt").read_text()[:800], end="")')
for scheme in progressive autokey; do
  cipher=$(RUST_LOG=warn cargo run --quiet -p vigenere -- encrypt \
    --scheme "$scheme" --alphabet ru-no-yo --key 'КЛЮЧ' --text "$plain")
  RUST_LOG=warn cargo run --quiet -p vigenere -- break "$cipher" \
    --scheme "$scheme" --alphabet ru-no-yo --min-key 2 --max-key 8
done
# В обоих случаях ожидается «Восстановленный ключ: КЛЮЧ».
```

Вместо `ru-no-yo` можно выбрать `en` или `ru-yo`: криптоанализ поддерживает
все три алфавита и все три схемы. Он основан на статистике букв и биграмм;
на коротком или нетипичном тексте найденный кандидат может быть неверным.
Для просмотра промежуточных оценок используйте `RUST_LOG=info` или просто
уберите `RUST_LOG=warn`; по умолчанию используется уровень `INFO`.

## Тесты и отчёты

```bash
cargo test -p vigenere
python3 scripts/vigenere/build.py
python3 scripts/lab_04_vigenere/build.py
```

Первый генератор создаёт отчёт за 2026 год в `docs/reports/2026/vigenere/`,
второй — отчёты вариантов лабораторной №4 за 2025 год в
`docs/reports/2025/lab_04_vigenere/`. Для генерации нужны `python-docx` и
`lxml`; примеры отчёта запускают реальный Rust CLI.
