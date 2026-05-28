# ПР2 — встраивание стеганографического сокрытия в docx

Программа берёт «голый» текстовый контейнер (любой docx со стихом или
строку), кодирует секретное сообщение выбранной кодировкой и записывает
новый docx, где для каждого бита назначено своё значение параметра
форматирования (размер шрифта, цвет, масштаб, интервал и т.д.).

## Запуск

```bash
uv sync --extra dev

# встроить в стих-контейнер из covers/
./.venv/bin/steganography text-format-encode encode \
    -s "Без труда не вытащишь и рыбку из пруда." \
    --cover-file resources/steganographic_concealment/covers/1.docx \
    -e cp866 -p size \
    -o /tmp/out.docx

# встроить в произвольный текст
./.venv/bin/steganography text-format-encode encode \
    -s "Секрет" \
    --cover-text "Текст любого размера, главное чтобы хватало символов." \
    -e Windows-1251 -p color \
    -o /tmp/out.docx

# пользовательские значения форматирования
./.venv/bin/steganography text-format-encode encode \
    -s "Hi" --cover-text "$(python -c 'print("a"*200)')" \
    -e ASCII -p spacing --zero 0 --one 10 \
    -o /tmp/out.docx
```

Поддерживаемые опции:

| Опция | Значения |
|------|----------|
| `-e/--encoding` | `МТК-2 (Бодо)`, `КОИ-8R`, `cp866`, `Windows-1251`, `ASCII` |
| `-p/--param` | `color`, `highlight`, `size`, `scale`, `spacing` |

Если `--zero/--one` не заданы, берутся незаметные пары по умолчанию
(например, для `size` — `28` и `29`, т.е. 14pt и 14.5pt).

## Массовая генерация 25 вариантов

```bash
./.venv/bin/python scripts/text_format_encode/generate_variants.py
```

Создаёт `resources/steganographic_concealment/generated/variant01.docx` …
`variant25.docx` — по таблице пословиц/методов/кодировок, циклически
переиспользуя cover-стихи из `covers/`.

## Сборка docx-отчётов по всем 25 вариантам

```bash
./.venv/bin/python scripts/text_format_encode/build.py
```

Результат: `docs/reports/2025/2/<N>/ПР2.docx` для каждого варианта N = 1..25.
В каждом отчёте — реальный прогон встраивания заданной пословицы в
cover-стих covers/<cover_index>.docx.

## Тесты (включая encode → decode roundtrip)

```bash
./.venv/bin/python -m pytest tests/unit/domain/text_format_encode \
    tests/unit/application/text_format_encode tests/integration/text_format_encode
```

## Архитектура

- `domain/common/encodings/` — общие кодировки с методом `encode(text)`.
- `domain/text_format_encode/value_objects/` — `SecretPayload`,
  `CharFormatting`, `FormattingPlan`.
- `domain/text_format_encode/services/` — `ContainerPlanBuilder` (текст →
  биты → план форматирования), `HidingValueDefaults`.
- `domain/text_format_encode/errors/` — `ContainerTooSmallError`,
  `UnencodableSecretError`.
- `infrastructure/text_format_encode/` — `DocxContainerWriterImpl` (запись
  через `python-docx` + прямые OOXML-элементы) и `DocxCoverTextReaderImpl`.
- `application/commands/text_format_encode/encode.py` — `EncodeSecretCommand`
  + handler.
- `presentation/cli/handlers/text_format_encode.py` — click-команда `encode`
  с инжектом через `dishka`.
