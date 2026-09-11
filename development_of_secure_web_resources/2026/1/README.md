# Лабораторная работа № 1 — Flask

**Ковалев Данил Петрович, ВКБ53.** Проверяющий: Ковальчик Р. В.

Домашняя страница приложения «Технологические расчёты доменной плавки»:
семантический HTML, справочная таблица с рисунка 2 методички, навигация и копирайт.
`/tempr` — заготовка следующей части; формулы расчёта в предоставленном PDF нет.

## Запуск в Docker

Нужен запущенный Docker с Compose v2. Команды выполняются из этого каталога:

```sh
docker compose up --build -d --wait
```

Открыть <http://127.0.0.1:5001>. Контейнер запускает Gunicorn с двумя процессами,
без debug, от непривилегированного пользователя. Healthcheck проверяет главную
страницу. Порт 5001 выбран с учётом возможного конфликта macOS AirPlay с 5000.

```sh
docker compose logs -f app
docker compose down
```

Для изменения порта или имени автора можно скопировать `.env.example` в `.env`.
Compose читает этот файл автоматически; обычный Python-запуск использует
переменные окружения, а не загружает `.env` самостоятельно.

Режим разработки с подключением `src` и автоматической перезагрузкой:

```sh
docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build -d --wait
```

Остановка — `docker compose down`. После изменения зависимостей пересоберите образ.
Режим debug предназначен только для локальной разработки; порт Compose привязан
к `127.0.0.1`.

## Локальный запуск через uv

```sh
uv sync --frozen
uv run blast-furnace run --port 5001
```

Окружение `.venv` создаёт и обслуживает только uv. Python — 3.14.
Активация окружения не нужна. В PyCharm выбрать интерпретатор `.venv/bin/python`.
Варианты запуска:

```sh
uv run python -m blast_furnace.app run --port 5001
uv run flask --app blast_furnace.app run --debug --port 5001
```

## Архитектура

```text
src/blast_furnace/
  app.py                         WSGI-точка входа
  domain/reference.py            предметная модель и справочные данные
  application/get_blast_reference.py  сценарий чтения справочника
  infrastructure/                место для будущих внешних адаптеров
  presentation/http/
    routes.py                    Blueprint, обработчики и форматирование чисел
    templates/                   base.html, index.html, tempr.html
    static/styles.css            адаптивное оформление
  setup/
    app_factory.py               сборка Flask и подключение Dishka
    config.py                    конфигурация
    ioc.py                       зависимости со Scope.REQUEST
    cli.py                       консольный запуск
tests/
  integration/presentation/http/ HTTP-проверки через Flask test client
  unit/setup/                    проверка конфигурации
deploy/Dockerfile                многостадийная сборка через uv
docs/                           отчёт и снимки экрана
```

Поток зависимостей: `presentation → application → domain`. Только `setup` собирает
приложение и DI. Внутренние слои не импортируют Flask и Dishka; правила проверяет
`.importlinter`. Инфраструктурные адаптеры пока не нужны: в ЛР1 нет БД или внешних
систем. Справочник неизменяемый, числа представлены `Decimal`; запятая добавляется
при отображении. Единицы и знаки изменений не придуманы: в исходной таблице их нет.

## Проверки

```sh
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run bandit -c pyproject.toml -r src
uv run lint-imports
uv run pytest --cov --cov-report=term-missing
```

Если установлен `just`: `just check`. Другие команды: `just run`, `just dev`,
`just up`, `just up-dev`, `just down`, `just logs`.

Тесты проверяют точные строки таблицы из задания, семантическую разметку,
навигацию и CSS, `/tempr`, ответы 404/405, экранирование имени автора,
изоляцию конфигурации и выключенный по умолчанию debug.

## Соответствие методичке

| Требование | Реализация |
|---|---|
| Виртуальное окружение | `.venv`, создано через uv по требованию пользователя |
| Установка Flask | `pyproject.toml` и `uv.lock` |
| Фиксация зависимостей | `uv.lock` + экспорт `requirements.txt` |
| `app.py` | `src/blast_furnace/app.py`, согласно выбранной src-структуре |
| `templates/index.html`, `tempr.html` | Каталог `presentation/http/templates` |
| `header`, `nav`, `main`, `footer` | Общий шаблон `base.html` |
| Справочная таблица | Все три строки рисунка 2, без изменения значений |
| GET `/` | Blueprint `pages`, шаблон `index.html` |
| Ссылка `/tempr` | Рабочая страница-заготовка с пояснением |
| Автор и год | Ковалев Данил Петрович; текущий год |
| Отладочный запуск | Явный `--debug` или Compose dev |

`requirements.txt` создаётся только через uv; редактировать его вручную не нужно:

```sh
uv export --frozen --no-dev --no-emit-project --format requirements-txt --output-file requirements.txt
```

Проект находится в существующем репозитории `DSTU_VKB`, поэтому отдельный вложенный
репозиторий не создаётся. Для фиксации работы из текущего каталога:

```sh
git add .
git commit -m "ЛР1: Flask-приложение технологических расчётов"
```

## Источники

Отчёт: `docs/Ковалев Д.П. ВКБ53 ЛР1.docx` и одноимённый PDF.
Исходники генератора и снимков сохранены в `tools/`:

```sh
uv sync --frozen --group report
uv run --group report python tools/capture_pages.py
uv run --group report python tools/build_report.py
```

Для снимков нужен Google Chrome и приложение на порту 5001.
Группа `report` не устанавливается в Docker-образ. PDF экспортирован из DOCX
через Microsoft Word; после пересборки DOCX экспорт PDF нужно повторить.

- Задание: `Laboratornaya_rabota_1_Razrabotka_Web_prilozhenia.pdf`, страницы 3–9.
- [Flask: фабрика приложения](https://flask.palletsprojects.com/en/stable/tutorial/factory/).
- [Dishka: интеграция Flask](https://dishka.readthedocs.io/en/stable/integrations/flask.html).
- [uv в Docker](https://docs.astral.sh/uv/guides/integration/docker/).
- [Flask и Gunicorn](https://flask.palletsprojects.com/en/stable/deploying/gunicorn/).
