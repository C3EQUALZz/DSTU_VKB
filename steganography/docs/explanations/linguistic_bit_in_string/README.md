# ПР3 — лингвистическое сокрытие одного бита в строке

Программа классифицирует каждую входную строку как «ДА» (бит = 1) или
«НЕТ» (бит = 0). Используемый лингвистический параметр — чётность числа
русских гласных букв в строке (полное описание — в файле
[`method.txt`](method.txt)).

## Запуск

```bash
uv sync --extra dev

# вход — текстовый файл (по одной строке на запись), выход — текстовый файл
./.venv/bin/steganography linguistic-bit-in-string classify \
    -i resources/linguistic_samples/input.txt \
    -o resources/linguistic_samples/output.txt
```

CLI выводит сводную PrettyTable-таблицу на экран и сохраняет результаты в
выходной файл (формат: `<ответ>\t<число_гласных>\t<строка>`).

## Эталонный набор 10 + 10

В `resources/linguistic_samples/input.txt` лежат ровно 10 строк, для
которых программа отвечает «ДА» (чётное число гласных), и 10 строк с
ответом «НЕТ» (нечётное число гласных), как требует условие.

## Сборка docx-отчёта

```bash
./.venv/bin/python scripts/linguistic_bit_in_string/build.py
```

Результат: `docs/reports/2025/3/ПР3.docx`.

## Тесты

```bash
./.venv/bin/python -m pytest \
    tests/unit/domain/linguistic_bit_in_string \
    tests/unit/application/linguistic_bit_in_string \
    tests/integration/linguistic_bit_in_string
```

## Архитектура

- `domain/linguistic_bit_in_string/services/vowel_counter.py` — подсчёт
  гласных в строке.
- `domain/linguistic_bit_in_string/services/parity_classifier.py` —
  отнесение строки к Y или N по чётности числа гласных.
- `domain/linguistic_bit_in_string/ports/` — Protocol-порты
  `StringReader` и `ClassificationWriter`.
- `infrastructure/linguistic_bit_in_string/` — реализации портов для
  обычных UTF-8 файлов.
- `application/commands/linguistic_bit_in_string/classify.py` — async
  Command Handler.
- `presentation/cli/handlers/linguistic_bit_in_string.py` — click-команда
  `classify` с инжектом через dishka.
