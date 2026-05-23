# Лаб 5 — Проверка кода SonarQube'ом

**Файлы:** `docker/sonarqube/compose.yaml`, `crates/lab_*/sonar-project.properties`, `scripts/sonar-scan-all.sh`.
**Статус:** ✅ инфраструктура готова — compose валидируется через `docker compose config`, scripts и properties на месте. Сам прогон сканирования требует Docker'а на машине и нескольких минут — оставлен пользователю.

## Условие

> Выполнить проверку исходных текстов программ по лабораторным 1-4 с использованием SonarQube. Каждая лабораторная должна быть представлена в виде отдельного проекта.
> Продемонстрировать результаты проверки.
> При нахождении критических и/или блокирующих замечаний, и замечаний касающихся безопасности приложения предложить варианты устранения этих замечаний.

## Как организовано

| Компонент | Файл | Назначение |
|-----------|------|-----------|
| Контейнеры | `docker/sonarqube/compose.yaml` | SonarQube CE 10.6 + PostgreSQL 16 в одной compose-сети. Healthcheck'и для readiness. |
| Креды БД | задано в compose | `sonar / sonar / sonarqube`. |
| Токен | `.env` в корне (см. `docker/sonarqube/.env.example`) | `SONAR_HOST_URL`, `SONAR_TOKEN` (генерится в UI). |
| `sonar-project.properties` | по одному в каждом `crates/lab_0X_*/` | `projectKey = lab_0X_*`, `sonar.sources=src`, `sonar.tests=tests`, импорт clippy.json. |
| Скрипт прогона | `scripts/sonar-scan-all.sh` | Запускает `cargo clippy --message-format=json`, фильтрует по крейту, вызывает `sonar-scanner` в каждом. |

Каждый крейт = **отдельный проект в SonarQube** — это требование условия и удобно для разбора замечаний.

## Как запустить

### 0. Один раз — установить инструменты

| ОС | Команда |
|----|---------|
| macOS | `brew install --cask docker && brew install sonar-scanner` |
| Linux (Ubuntu) | `sudo apt install docker.io docker-compose-plugin && # sonar-scanner — см. ссылку ниже` |
| Любая | [`sonar-scanner` бинарь](https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/) |

### 1. Поднять SonarQube и инициализировать его

**Быстрый путь — одной командой** (рекомендуется):

```bash
just sonar-init
# = sonar-up + sonar-bootstrap
```

`sonar-init` сделает всё за вас:
1. Поднимет контейнеры (compose up -d).
2. Подождёт пока SonarQube ответит `api/system/status = UP` (до ~3 минут).
3. Сменит пароль `admin/admin` → `admin/psia-admin-2026` (можно переопределить через `SONAR_ADMIN_PASSWORD=…`).
4. Сгенерирует пользовательский токен `psia-scan`.
5. Создаст 4 проекта: `lab_01_rsa`, `lab_02_sha256`, `lab_03_prng`, `lab_04_nist`.
6. Запишет `SONAR_HOST_URL` / `SONAR_TOKEN` / `SONAR_ADMIN_PASSWORD` в `.env` (с `chmod 600`).

Идемпотентно — повторный запуск ничего не сломает.

> **Ручной путь** (только если автонастройка не подходит): см. конец документа, [«Ручная настройка»](#ручная-настройка-если-не-нравится-bootstrap).

### 2. Запустить сканирование

```bash
just sonar-scan-all
# Эквивалент: ./scripts/sonar-scan-all.sh
```

Скрипт:
1. Прогоняет `cargo clippy --workspace --message-format=json --all-targets` → `/tmp/clippy-workspace.json`.
2. Для каждой `lab_*` фильтрует замечания clippy по её имени → `crates/<lab>/clippy.json`.
3. Запускает `sonar-scanner` из каталога крейта.

В UI SonarQube под каждым `projectKey` появятся:
- метрики Quality Gate (bugs / vulnerabilities / code smells / coverage);
- список замечаний с тяжестью BLOCKER / CRITICAL / MAJOR / MINOR / INFO.

### 3. Остановить

```bash
just sonar-down
# или с удалением данных:  docker compose -f docker/sonarqube/compose.yaml down -v
```

## Замечания / план устранения

Заполняется после первого прогона. Шаблон записи:

| Лаба | Severity | Правило (Sonar / Clippy) | Файл:строка | План устранения |
|------|----------|---------------------------|-------------|------------------|
| (пример) lab_01_rsa | CRITICAL | `clippy::expect_used` | `src/foo.rs:42` | заменить `.expect(…)` на `?` |
| ... | ... | ... | ... | ... |

Для замечаний категории **Security** — кратко описать модель угроз и зафиксировать в этом разделе ровно то, чего просит условие («предложить варианты устранения»).

## Что НЕ покрывает эта лаба

- Реальный CI-прогон в облаке (SonarCloud / GitHub Actions). Если потребуется — добавить workflow с `sonarqube-scan-action`.
- Code coverage (`sonar.community.rust.lcov.reportPaths`). Подключить через `cargo-llvm-cov` или `cargo-tarpaulin`, если этого захочет преподаватель.

## Ручная настройка (если не нравится bootstrap)

1. `just sonar-up`, подождать пока UI ответит на `http://localhost:9000`.
2. Логин `admin / admin`, при первом входе сменить пароль.
3. Profile → **My Account → Security → Generate Tokens** → имя `psia-scan` → **Generate**. Скопировать.
4. Создать `.env` в корне:
   ```bash
   cat > .env <<EOF
   SONAR_HOST_URL=http://localhost:9000
   SONAR_TOKEN=<вставить токен>
   EOF
   chmod 600 .env
   ```
5. Создать 4 проекта вручную через **Projects → Create Project → Manually** или через API:
   ```bash
   source .env
   for KEY in lab_01_rsa lab_02_sha256 lab_03_prng lab_04_nist; do
     curl -sS -u "$SONAR_TOKEN:" -X POST \
       "$SONAR_HOST_URL/api/projects/create?name=$KEY&project=$KEY"
     echo
   done
   ```

## Полезное

- Лог-файл SonarQube: `docker logs psia-sonarqube` или `/opt/sonarqube/logs/sonar.log` в томе `sonarqube_logs`.
- Постгрес-том: `sonar_db_data`. Уничтожить вместе с проектом: `docker compose ... down -v`.
- Сменить порт: добавить `9001:9000` в маппинг и обновить `SONAR_HOST_URL` в `.env`.
