# Shape Vision

Приложение состоит из двух сервисов:

- `backend`: FastAPI + PyTorch, обучение и предсказание фигуры по изображению.
- `frontend`: React + Vite, интерфейс загрузки изображения и показа результата.

## Настройка `.env`

По умолчанию рабочий файл уже добавлен:

```text
.env
```

Если захочешь изменить порты или путь хранения артефакта, отредактируй его. Для нового окружения можно взять шаблон:

```bash
cp .env.example .env
```

Главные параметры:

- `BACKEND_PORT`: порт FastAPI на хосте
- `FRONTEND_PORT`: порт React/Nginx на хосте
- `BACKEND_ARTIFACTS_DIR`: куда на хосте сохранять обученную модель
- `IMAGE_ANALYZER_DB_URL`: адрес БД backend, по умолчанию SQLite-файл в `backend/artifacts`
- `IMAGE_ANALYZER_ALLOW_ORIGINS`: CORS origin для frontend

Если меняешь `FRONTEND_PORT`, не забудь поставить такой же адрес в `IMAGE_ANALYZER_ALLOW_ORIGINS`.

## Запуск одной командой

```bash
docker compose up --build
```

После запуска:

- frontend: `http://localhost:8080`
- backend API: `http://localhost:8000`
- backend docs: `http://localhost:8000/docs`

При старте backend теперь автоматически:

- при необходимости обучает модель
- применяет миграции Alembic
- открывает SQLite-базу в `backend/artifacts/image_analyzer.db`

При повторных запусках достаточно:

```bash
docker compose up
```

## Автоматическое обучение модели

При старте backend-контейнера проверяется наличие файла:

```text
backend/artifacts/shape_classifier.pt
```

Если файла нет, контейнер автоматически запускает обучение на датасете из:

```text
backend/hw_light
```

и сохраняет артефакт в `backend/artifacts`.

Если хочешь принудительно переобучить модель, просто удали файлы:

```bash
rm -f backend/artifacts/shape_classifier.pt backend/artifacts/shape_classifier.json
docker compose up --build
```

История запросов к распознаванию сохраняется в БД и доступна через:

```text
GET /api/v1/predictions
```

## Структура

- `backend/`: ML backend и API
- `frontend/`: React интерфейс
- `deploy/`: Dockerfile и конфиги деплоя
- `docker-compose.yml`: запуск всего стека
- `.env`: текущая конфигурация compose
- `.env.example`: шаблон конфигурации
