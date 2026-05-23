# Лаб 5 — Проверка кода SonarQube'ом

**Crate:** нет (это инфраструктурная лаба).
**Файлы:** `docker/sonarqube/compose.yaml`, `crates/*/sonar-project.properties`.
**Статус:** ⏳ в разработке

## Условие

> Выполнить проверку исходных текстов программ по лабораторным 1-4 с использованием SonarQube. Каждая лабораторная должна быть представлена в виде отдельного проекта.
> Продемонстрировать результаты проверки.
> При нахождении критических и/или блокирующих замечаний, и замечаний касающихся безопасности приложения предложить варианты устранения этих замечаний.

## Подход

1. Поднимаем **SonarQube Community Edition** локально через Docker Compose. PostgreSQL — встроенный сервис в той же compose-сети, чтобы не зависеть от системного.
2. Каждая лаба — отдельный проект (`projectKey = lab_XX_<name>`). Сборка workspace гарантирует, что `crates/<name>/` содержит ровно код этой лабораторной — поэтому Sonar сканирует именно «отдельный проект».
3. Анализ — через `sonar-scanner` CLI. У каждой лабы свой `sonar-project.properties`.

> Rust-плагина в Community Edition нет, но Community **умеет** работать с произвольными языками через SonarQube «Generic Issue Format». Параллельно подключим [community-rust](https://github.com/elegoff/sonar-rust) — open-source плагин с поддержкой Rust (через clippy-импорт).

## Как запустить

```bash
# 1) Поднимаем SonarQube
just sonar-up
# подождать ~1 мин до readiness, затем открыть http://localhost:9000

# 2) Логин admin/admin, сменить пароль, создать токен (My Account → Security)
echo "SONAR_TOKEN=<новый_токен>" >> .env

# 3) Создать проекты через UI или через API:
for c in lab_01_rsa lab_02_sha256 lab_03_prng lab_04_nist; do
  curl -u $SONAR_TOKEN: -X POST \
    "http://localhost:9000/api/projects/create?name=$c&project=$c"
done

# 4) Установить sonar-scanner: `brew install sonar-scanner`

# 5) Прогон по каждой лабе
just sonar-scan lab_01_rsa
just sonar-scan lab_02_sha256
just sonar-scan lab_03_prng
just sonar-scan lab_04_nist

# 6) Останов
just sonar-down
```

## Что лежит в `sonar-project.properties` каждого крейта

```properties
sonar.projectKey=lab_XX_<name>
sonar.projectName=Лабораторная № X — <название>
sonar.projectVersion=0.1.0
sonar.sources=src
sonar.tests=tests
sonar.sourceEncoding=UTF-8
sonar.language=rust

# Импорт clippy через community-rust (предварительно сгенерировать clippy.json)
sonar.community.rust.clippy.reportPaths=clippy.json
```

Перед сканированием прогоняем clippy в JSON:

```bash
cargo clippy --message-format=json -- -W clippy::all > crates/lab_01_rsa/clippy.json
```

## Анализ замечаний и план устранения

После прогона записывать сюда:

| Лаба | Severity | Правило | Файл:строка | План устранения |
|------|----------|---------|-------------|------------------|
| lab_01_rsa | BLOCKER | clippy::expect_used | src/foo.rs:42 | заменить на `?` |
| ... | ... | ... | ... | ... |

(Заполнится после первого прогона.)
