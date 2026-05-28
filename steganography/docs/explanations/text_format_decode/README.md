# ПР1 — декодирование стеганографического сокрытия в docx

Программа определяет, по какому параметру форматирования (цвет, цвет фона,
размер шрифта, масштаб, межсимвольный интервал) скрыто секретное сообщение
в `.docx`-документе, выбирает кодировку (МТК-2, КОИ-8R, cp866, Windows-1251,
ASCII) и восстанавливает текст.

## Запуск

```bash
# создать виртуальное окружение (uv должен быть установлен)
uv sync --extra dev

# одиночный файл
./.venv/bin/steganography text-format-decode detect \
    -f resources/steganographic_concealment/variants/variant15.docx

# пакетный анализ каталога
./.venv/bin/steganography text-format-decode detect-all \
    -d resources/steganographic_concealment/variants/

# подробные логи
./.venv/bin/steganography -v text-format-decode detect-all \
    -d resources/steganographic_concealment/variants/

# JSON-логи в pipe (через переменную окружения)
STEGANOGRAPHY_LOG_JSON=1 ./.venv/bin/steganography text-format-decode detect-all \
    -d resources/steganographic_concealment/variants/
```

## Сборка docx-отчёта

```bash
./.venv/bin/python scripts/text_format_decode/build.py
```

Результат: `docs/reports/text_format_decode/ПР1_декодирование.docx`.

## Тесты

```bash
./.venv/bin/python -m pytest tests/unit/domain/common tests/unit/domain/text_format_decode \
    tests/unit/application/text_format_decode tests/integration/text_format_decode
```

## Архитектура

- `domain/common/encodings/` — общие кодировки (двунаправленные).
- `domain/text_format_decode/services/` — детектор метода форматирования,
  декодер сообщения, утилиты битовой строки.
- `domain/text_format_decode/language/` — частотная статистика русского
  языка для скоринга кандидатов.
- `application/commands/text_format_decode/decode.py` — `DetectSecretCommand`
  + handler.
- `infrastructure/text_format_decode/docx_reader.py` — чтение docx через
  `lxml`.
- `presentation/cli/handlers/text_format_decode.py` — click-команды
  `detect`/`detect-all` с инжектом через `dishka`.
