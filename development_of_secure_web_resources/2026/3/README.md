# SecureDev · Лабораторная работа № 3

Приложение на Flask продолжает расчёты доменной плавки из ЛР2. Главная страница открыта всем. Расчёт `/tempr` и сравнение двух режимов `/compare` доступны после регистрации или входа.

## Запуск

Из каталога лабораторной, с Python 3.14 и `uv` на macOS или Linux (на Windows — в WSL):

```sh
uv sync --locked
export SECRET_KEY="$(uv run --no-sync python -c 'import secrets; print(secrets.token_hex(32))')"
uv run --no-sync alembic upgrade head
uv run --no-sync blast-furnace run --host 127.0.0.1 --port 5003
```

Откройте <http://127.0.0.1:5003>. Регистрироваться можно с учебным адресом вида `anna@example.org`. Для проверки после перезапуска используйте тот же `SECRET_KEY` и путь к БД. Команда генерации создаёт новый ключ при каждом выполнении.

| Переменная | Назначение | Значение по умолчанию |
| --- | --- | --- |
| `SECRET_KEY` | Случайный ключ подписи Flask и токенов форм | Требуется, от 32 символов |
| `DATABASE_PATH` | Путь к SQLite, общий для приложения и Alembic | `data/securedev.db` |
| `CALC_LOG_PATH` | Путь к журналу | `logs/calc_log.txt` |
| `SESSION_COOKIE_SECURE` | Значение `1` включает отправку cookie по HTTPS | Выключено для локального HTTP |
| `AUTHOR_NAME` | Имя автора в подвале страницы | Ковалев Данил Петрович |

## Проверка

```sh
uv run --no-sync pytest --cov --cov-report=term-missing
uv run --no-sync ruff format --check .
uv run --no-sync ruff check .
uv run --no-sync mypy
uv run --no-sync bandit -c pyproject.toml -r src
uv run --no-sync lint-imports
uv run --no-sync alembic check
```

Гость получает перенаправление с обеих расчётных страниц. Регистрация сохраняет имя, email и хеш PBKDF2 со случайной солью. Вход создаёт новый сеанс в SQLite, а выход по POST с токеном формы удаляет текущий сеанс. Обращение к странице запускает удаление сеансов, проживших один час. Срок отсчитывается от создания сеанса.

Тесты применяют миграции к временной БД. Интеграционный тест переводит часы вперёд и проверяет отказ после истечения часа и удаление записи при запросе.

Отчёт и снимки находятся в `docs/`. При установленном Google Chrome их можно пересоздать командами `uv sync --locked --group report`, `uv run --no-sync python tools/capture_pages.py` при запущенном приложении, затем `uv run --no-sync python tools/build_report.py`.
