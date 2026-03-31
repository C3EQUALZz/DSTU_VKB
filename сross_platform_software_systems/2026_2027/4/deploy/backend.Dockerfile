FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /opt/venv
RUN pip install --no-cache-dir --upgrade pip uv

COPY backend/pyproject.toml /app/pyproject.toml
COPY backend/uv.lock /app/uv.lock
COPY backend/README.md /app/README.md
COPY backend/src /app/src
COPY backend/hw_light /app/hw_light

RUN uv sync --frozen --no-dev

COPY deploy/backend-entrypoint.sh /usr/local/bin/backend-entrypoint.sh
RUN chmod +x /usr/local/bin/backend-entrypoint.sh

ENV IMAGE_ANALYZER_DATA_DIR=/app/hw_light \
    IMAGE_ANALYZER_MODEL_PATH=/app/artifacts/shape_classifier.pt \
    IMAGE_ANALYZER_ALLOW_ORIGINS=http://localhost:8080

EXPOSE 8000

ENTRYPOINT ["backend-entrypoint.sh"]
