# Программирование алгоритмов защиты информации

Курс лабораторных по дисциплине «Программирование алгоритмов защиты информации» (ДГТУ, ВКБ). 1 практическая + 7 лабораторных работ, реализованных на **Rust** в виде [Cargo workspace](#структура-репозитория).

> Условия преподавателя — в [`docs/conditions/`](docs/conditions). Поясняющие README по каждой работе — в [`docs/explanations/`](docs/explanations). Внутренние заметки агентам — в [`AGENTS.md`](AGENTS.md).

## Список работ

| №          | Crate / каталог                                | Тема                                                   | Инструкция                                                                            |
|------------|------------------------------------------------|--------------------------------------------------------|---------------------------------------------------------------------------------------|
| Практика 1 | [`crates/practice_01`](crates/practice_01)     | Длинная арифметика (≥ 64 разрядов), сложение/вычитание | [`docs/explanations/practice_01/`](docs/explanations/practice_01/README.md)           |
| Лаб 1      | [`crates/lab_01_rsa`](crates/lab_01_rsa)       | RSA с нуля                                             | [`docs/explanations/lab_01_rsa/`](docs/explanations/lab_01_rsa/README.md)             |
| Лаб 2      | [`crates/lab_02_sha256`](crates/lab_02_sha256) | SHA-2-256 по FIPS 180-4                                | [`docs/explanations/lab_02_sha256/`](docs/explanations/lab_02_sha256/README.md)       |
| Лаб 3      | [`crates/lab_03_prng`](crates/lab_03_prng)     | ПДСЧ + проверка через NIST STS 2.1.2                   | [`docs/explanations/lab_03_prng/`](docs/explanations/lab_03_prng/README.md)           |
| Лаб 4      | [`crates/lab_04_nist`](crates/lab_04_nist)     | Свой тест из NIST SP 800-22                            | [`docs/explanations/lab_04_nist/`](docs/explanations/lab_04_nist/README.md)           |
| Лаб 5      | [`docker/sonarqube`](docker/sonarqube)         | Прогон лаб 1-4 через SonarQube                         | [`docs/explanations/lab_05_sonarqube/`](docs/explanations/lab_05_sonarqube/README.md) |
| Лаб 6      | [`crates/lab_06_sym`](crates/lab_06_sym)       | Симметричное шифрование (Security framework)           | [`docs/explanations/lab_06_sym/`](docs/explanations/lab_06_sym/README.md)             |
| Лаб 7      | [`crates/lab_07_asym`](crates/lab_07_asym)     | Асимметричное шифрование (Security framework)          | [`docs/explanations/lab_07_asym/`](docs/explanations/lab_07_asym/README.md)           |

## Системные требования

| Что                                | Версия                | Зачем                                                                                                                             |
|------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| **Rust**                           | ≥ 1.85 (edition 2024) | Сборка workspace                                                                                                                  |
| **Cargo**                          | приходит с rustup     | Сборка/тесты                                                                                                                      |
| **just**                           | ≥ 1.40                | Удобные команды (`just lint`, `just lab-01`, …)                                                                                   |
| **Docker** + **Docker Compose v2** | любой свежий          | Лаб 5: SonarQube + Postgres                                                                                                       |
| **Python 3**                       | ≥ 3.9                 | Только для `pre-commit` и `just read-conditions`                                                                                  |
| **Sonar Scanner CLI**              | ≥ 5.0                 | Лаб 5                                                                                                                             |
| **Make + GCC/clang**               | системные             | Сборка `sts-2.1.2` для лаб 3                                                                                                      |
| **macOS**                          | 12+                   | Лаб 6 и 7 (Security framework). На Linux/Windows эти две лабы не соберутся в текущем варианте — потребуется отдельная реализация. |

## Установка зависимостей с нуля (macOS)

```bash
# 1. Rust toolchain (если ещё нет)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
rustup toolchain install stable
rustup component add clippy rustfmt

# 2. just (task runner)
brew install just

# 3. Docker Desktop — скачать с https://www.docker.com/products/docker-desktop/
#    или: brew install --cask docker

# 4. SonarScanner (для лаб 5)
brew install sonar-scanner

# 5. (опц.) pre-commit на Python
pip3 install --user pre-commit

# 6. (для лаб 3) если не установлены — Xcode CLT (там make/clang)
xcode-select --install
```

## Установка с нуля (Linux, например Ubuntu)

```bash
# Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
rustup component add clippy rustfmt

# just
cargo install just                  # или sudo apt install just (24.04+)

# Docker + Compose
sudo apt update
sudo apt install -y docker.io docker-compose-plugin

# SonarScanner
# https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/

# build essentials
sudo apt install -y build-essential python3 unzip
```

> Лаб 6 и 7 на Linux потребуют адаптации (использовать OpenSSL через системный пакет вместо Security framework). По умолчанию они помечены `#[cfg(target_os = "macos")]`.

## Первый запуск

```bash
git clone <repo> && cd programming_of_information_security_algorithms

# 1) проверить toolchain
cargo --version       # 1.85+
just --version        # 1.40+

# 2) собрать всё
cargo build --workspace

# 3) прогон ворот качества
just ci               # = fmt-check + lint + test

# 4) (опц.) повесить git pre-commit hook
just install-hooks
# или вариант через pre-commit:
just install-prek
```

## Удобные команды (из `justfile`)

```bash
just                     # список всех целей
just fmt                 # cargo fmt
just lint                # clippy с -D warnings
just test                # cargo test
just ci                  # fmt-check + lint + test
just docs                # cargo doc --open

# Запуск работ
just practice-01 add 12345 67890
just lab-01 gen --bits 1024 --public artifacts/lab_01/public.key --private artifacts/lab_01/private.key
just lab-02 hash README.md --out artifacts/lab_02/readme.sha256
just lab-03 gen --count 200 --seed 0xDEADBEEFCAFEBABE --out-bin artifacts/lab_03/sequence.bin --out-ascii artifacts/lab_03/sequence.bits
just lab-04 check --input artifacts/lab_03/sequence.bits --out artifacts/lab_04/report.txt
just lab-06 gen-key --out artifacts/lab_06/symm.key
just lab-07 gen-keys --public artifacts/lab_07/pub.der --private artifacts/lab_07/priv.der

# Лаб 5 (SonarQube)
just sonar-up                   # docker compose up -d
just sonar-scan lab_01_rsa      # sonar-scanner для одной лабы
just sonar-down
```

## Логирование

Все CLI используют `tracing` через `shared::logging::init()`. Уровень — `RUST_LOG`:

```bash
RUST_LOG=info just lab-01 gen ...     # по умолчанию
RUST_LOG=debug just lab-01 gen ...    # подробности алгоритма
RUST_LOG=trace just lab-01 gen ...    # пошагово (но трогает приватные данные!)
RUST_LOG="lab_01_rsa=debug,info" ...  # точечно
```

Формат — pretty (цветной, многострочный). Ошибки — через `color-eyre` с backtrace при `RUST_BACKTRACE=1`.

## Структура репозитория

```
.
├── README.md                       ← ты здесь
├── AGENTS.md                       ← заметки для Claude / контрибьюторов
├── Cargo.toml                      ← virtual manifest workspace
├── rustfmt.toml
├── justfile                        ← команды
├── .pre-commit-config.yaml
├── .gitignore
├── crates/
│   ├── shared/                     ← общая инфраструктура (логгер, ошибки)
│   ├── practice_01/                ← Практика 1
│   ├── lab_01_rsa/                 ← Лаб 1
│   ├── lab_02_sha256/              ← Лаб 2
│   ├── lab_03_prng/                ← Лаб 3
│   ├── lab_04_nist/                ← Лаб 4
│   ├── lab_06_sym/                 ← Лаб 6
│   └── lab_07_asym/                ← Лаб 7
├── docker/
│   └── sonarqube/                  ← Лаб 5 — compose.yaml
├── docs/
│   ├── conditions/                 ← .docx с условиями от преподавателя
│   └── explanations/               ← подробные README по каждой работе
│       ├── practice_01/
│       ├── lab_01_rsa/
│       ├── lab_02_sha256/
│       ├── lab_03_prng/
│       ├── lab_04_nist/
│       ├── lab_05_sonarqube/
│       ├── lab_06_sym/
│       └── lab_07_asym/
└── artifacts/                      ← выходные файлы CLI (не в git)
```

## Архитектурные принципы

Каждая лаба следует **Clean Architecture**:

```
crates/lab_XX_*/
└── src/
    ├── domain/             ← чистые типы и алгоритмы (без std::fs, без tracing)
    ├── application/        ← use cases (orchestration)
    ├── infrastructure/     ← реализации портов (файлы, system API)
    ├── presentation/       ← CLI (clap)
    ├── lib.rs              ← модули
    └── main.rs             ← точка входа: shared::logging::init() + presentation::run()
```

Подробнее — в [AGENTS.md](AGENTS.md).

## Лицензия

MIT (см. [Cargo.toml](Cargo.toml)).
