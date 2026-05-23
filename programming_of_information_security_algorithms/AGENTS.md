# AGENTS.md — заметки для будущих сессий Claude

Этот файл — компаньон для агентов, работающих над курсом «Программирование алгоритмов защиты информации». Прочитай его прежде чем начинать любую работу в репозитории.

## 1. Что это за репозиторий

Курс из **1 практической** и **7 лабораторных** работ по криптографии, реализуемых на **Rust**. Студент — Danil Kovalev (ДГТУ, ВКБ).

Условия лежат в:
- `docs/conditions/1 Практика.docx`
- `docs/conditions/Laboratornye_po_kursu_Programmirovanie_algoritmov_zaschity_informatsii.docx`

Извлекать текст из `.docx` (без `pandoc`/`python-docx`):
```bash
unzip -p "<file>.docx" word/document.xml | python3 -c '
import sys, xml.etree.ElementTree as ET
ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
root = ET.fromstring(sys.stdin.read())
for p in root.iter(ns+"p"):
    print("".join(t.text or "" for t in p.iter(ns+"t")))
'
```

## 2. Архитектурные правила (строго!)

1. **Cargo workspace** — `Cargo.toml` в корне — virtual manifest. Каждая работа = отдельный crate в `crates/`. Так требует лаб 5 (SonarQube хочет отдельные проекты).
2. **Clean Architecture** в каждом крейте:
   - `domain/` — чистые типы и алгоритмы, без `std::fs`, `std::io`, `tracing` (логи в домене только через trait, если нужно).
   - `application/` — usecases, оркестрирует доменом и инфраструктурой через trait-абстракции.
   - `infrastructure/` — реализации портов (файлы, сторонние API).
   - `presentation/` — CLI (`clap`).
3. **Запрет на готовые крипто-крейты** там, где условие требует реализации с нуля:
   - Лаб 1 RSA — без `rsa`, `num-bigint`, `num-prime`. Big integer пишем сами.
   - Лаб 2 SHA-256 — без `sha2`, `ring`, `digest`. По FIPS 180-4.
   - Лаб 4 NIST — алгоритм теста пишем сами.
   - Практика 1 — длинная арифметика своими руками.
4. **Инфраструктура — можно**: `tracing`, `tracing-subscriber`, `color-eyre`, `clap`, `thiserror`, `proptest`, `froodi` (DI). `security-framework` разрешён в лаб 6/7 — это обёртка над системным API macOS, эквивалент «встроенного функционала ОС» (CRYPTOAPI на Windows).

## 3. Стек

- Rust **edition 2024** (rust-version = 1.85+).
- Логи: `tracing` + `tracing-subscriber` (pretty), инициализация через `shared::logging::init()`. Уровень — переменная `RUST_LOG`, по умолчанию `INFO`.
- Ошибки: `color-eyre::Result` в CLI; `thiserror` в доменных модулях.
- DI: `froodi` где компонентов реально много (CLI хост со сценариями). Чистая алгоритмика — обычное конструкторное внедрение.
- Тесты: `cargo test`, для криптографии — `proptest` и тестовые векторы стандартов (FIPS/NIST/RFC).

## 4. Правила качества (gate перед «готово»)

Любая работа считается готовой только после:

```bash
just fmt-check    # cargo fmt --all -- --check
just lint         # cargo clippy --workspace --all-targets -- -D warnings
just test         # cargo test --workspace --all-features
# или одной командой:
just ci
```

Все три команды должны быть зелёными. Без `--no-verify`, без `#[allow(...)]` без объяснения в коде.

### Локальные хуки

- `just install-hooks` ставит простой `.git/hooks/pre-commit`, вызывающий `just precommit`.
- `just install-prek` ставит [pre-commit](https://pre-commit.com) по `.pre-commit-config.yaml` (хуки: trailing-whitespace, eof-fixer, `cargo fmt --check`, `cargo clippy`; `cargo test` — на `pre-push`).

Pre-commit не запускает дорогие проверки на каждый коммит без нужды — `cargo test` вынесен в `pre-push`.

## 5. Логирование (важно!)

- Никаких `println!`/`eprintln!` в прод-коде (кроме явного вывода результата по требованию задания — например, «вывести расшифрованное сообщение на экран»).
- В CLI первая строка — `shared::logging::init()?`.
- Логи обильные, но осмысленные:
  - `info!` — границы операций (старт/конец usecase, ключевые промежуточные этапы).
  - `debug!` — внутренности алгоритма (раунды, ключевые материалы — но **никогда** приватные ключи целиком!).
  - `trace!` — пошаговые состояния (отдельные шаги Miller-Rabin, итерации SHA).
  - `warn!` — отклонения (повторный запуск Miller-Rabin при неудаче, неуверенный результат теста NIST).
  - `error!` — ошибки IO/формата.
- Использовать структурированные поля: `tracing::info!(bytes = data.len(), "hashing file");`, а не `format!`.

## 6. Структура repo

```
.
├── AGENTS.md                       # ты сейчас читаешь
├── Cargo.toml                       # virtual manifest
├── rustfmt.toml
├── crates/
│   ├── shared/                     # logger + общие ошибки
│   ├── practice_01/                # практика 1
│   ├── lab_01_rsa/                 # лаб 1
│   ├── lab_02_sha256/              # лаб 2
│   ├── lab_03_prng/                # лаб 3
│   ├── lab_04_nist/                # лаб 4
│   ├── lab_06_sym/                 # лаб 6 (macOS Security FW)
│   └── lab_07_asym/                # лаб 7 (macOS Security FW)
├── docker/
│   └── sonarqube/                  # лаб 5: compose.yaml + конфиг
├── docs/
│   ├── conditions/                 # docx с условиями
│   └── explanations/               # инструкции по каждой работе
│       ├── practice_01/README.md
│       ├── lab_01_rsa/README.md
│       └── ...
└── artifacts/                      # выходные файлы (ключи, шифртексты, хеши)
```

`artifacts/` создаётся при запуске и в git не коммитится.

## 7. Как добавлять новую работу

1. Создать `crates/<name>/Cargo.toml` со ссылками `*.workspace = true` и `[lints] workspace = true`.
2. Добавить `crates/<name>` в `Cargo.toml` → `[workspace] members`.
3. Внутри крейта — `src/domain/`, `src/application/`, `src/infrastructure/`, `src/presentation/`, `src/main.rs` или `bin/`.
4. Создать `docs/explanations/<name>/README.md` с разделами: условие, реализация, как запустить, как протестировать, входы/выходы.
5. Прогнать gate (см. §4).

## 8. Что НЕ делать

- Не использовать `unwrap()` / `expect()` в прод-коде. Clippy включён.
- Не складывать большие бинарные артефакты (`sts-2_1_2.zip`, `*.zip` ключей) в git.
- Не амэндить чужие коммиты; делать новые.
- Не править условия в `docs/conditions/` — они от преподавателя.
- Не подключать sha2/rsa/num-bigint/ring «для скорости» в крейтах с алгоритмами с нуля.

## 9. Лаб 5 (SonarQube) — порядок действий

1. `cd docker/sonarqube && docker compose up -d` — поднять SonarQube + Postgres.
2. Открыть `http://localhost:9000`, дефолт `admin/admin`, сменить пароль.
3. Создать токен в профиле → положить в `.env` под именем `SONAR_TOKEN`.
4. Для каждой лабы создать проект (UI или API) с `projectKey = lab_XX_<name>`.
5. Запустить sonar-scanner на корне workspace (`sonar-project.properties` в каждом крейте).
6. Зафиксировать критические/блокирующие замечания → описать в `docs/explanations/lab_05_sonarqube/README.md`.

## 10. Что отвечать пользователю

- На русском.
- Кратко, без воды. Что сделал — одной-двумя фразами; не пересказывать диффы.
- Если условие неоднозначное — спрашивать через AskUserQuestion, а не угадывать.
