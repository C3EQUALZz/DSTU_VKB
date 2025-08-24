FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
WORKDIR /app

ENV UV_COMPILE_BYTECODE 1
ENV UV_SYSTEM_PYTHON 1
ENV UV_NO_CACHE 1

COPY ./pyproject.toml ./deploy/dev/automatic_responses/telegram_entrypoint.sh ./deploy/dev/automatic_responses/worker_entrypoint.sh ./
COPY ./src ./src

RUN uv pip install --system --no-cache --target dependencies ".[dev]"


FROM python:3.12-slim AS production
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/app/dependencies"

RUN apt-get update && apt-get install -y curl

COPY --from=builder /app/ ./